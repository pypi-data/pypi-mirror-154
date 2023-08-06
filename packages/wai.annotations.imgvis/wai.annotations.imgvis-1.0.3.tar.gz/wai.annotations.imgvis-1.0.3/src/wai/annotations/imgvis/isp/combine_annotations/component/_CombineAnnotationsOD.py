from shapely.geometry import Polygon, GeometryCollection, MultiPolygon
from shapely.ops import unary_union

from wai.common.cli.options import TypedOption
from wai.common.geometry import Polygon as WaiPolygon
from wai.common.geometry import Point as WaiPoint
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance


UNION = "union"
INTERSECT = "intersect"
COMBINATIONS = [
    UNION,
    INTERSECT,
]

STREAM_INDEX = "stream_index"


def to_polygons(located_objects):
    """
    Turns the located objects into shapely polygons.

    :param located_objects: the objects to convert
    :type located_objects: LocatedObjects
    :return: the list of polygons
    :rtype: list
    """
    result = []
    for obj in located_objects:
        coords = []
        for point in obj.get_polygon().points:
            coords.append((point.x, point.y))
        result.append(Polygon(coords))
    return result


def intersect_over_union(poly1, poly2):
    """
    Calculates the IoU (intersect over union) for the two polygons.

    :param poly1: the first polygon
    :type poly1: Polygon
    :param poly2: the second polygon
    :type poly2: Polygon
    :return: the IoU
    :type: float
    """
    try:
        intersection = poly2.intersection(poly1)
        if intersection.area > 0:
                union = unary_union([poly2, poly1])
                return intersection.area / union.area
        else:
            return 0
    except:
        print("Failed to compute IoU!")
        return 0


class CombineAnnotationsOD(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which combines object detections into single one.
    """

    min_iou: float = TypedOption(
        "--min-iou",
        type=float,
        default=0.7,
        help="the minimum IoU (intersect over union) to use for identifying objects that overlap"
    )

    combination: str = TypedOption(
        "--combination",
        type=str,
        default=INTERSECT,
        help="how to combine the annotations (%s); the '%s' key in the meta-data contains the stream index" % ("|".join(COMBINATIONS), STREAM_INDEX)
    )

    def _find_matches(self, polygons_old, polygons_new):
        """
        Finds the matches between the old and new annotations.

        :param polygons_old: the old annotations
        :type polygons_old: list
        :param polygons_new: the new annotations
        :type polygons_new: list
        :return: the matches, list of old/new index tuples (an index of -1 means no match found)
        :rtype: list
        """
        result = []
        match_new = set([x for x in range(len(polygons_new))])
        match_old = set([x for x in range(len(polygons_old))])
        for n, poly_new in enumerate(polygons_new):
            for o, poly_old in enumerate(polygons_old):
                iou = intersect_over_union(poly_new, poly_old)
                if iou > 0:
                    if iou >= self.min_iou:
                        if n in match_new:
                            match_new.remove(n)
                        if o in match_old:
                            match_old.remove(o)
                        result.append((o, n, iou))

        # add old polygons that had no match
        for o in match_old:
            result.append((o, -1, 0.0))

        # add new polygons that had no match
        for n in match_new:
            result.append((-1, n, 0.0))

        return result

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_annotations"):
            self._annotations = element.annotations
            self._stream_index = 0
            then(element)
            return

        self._stream_index += 1

        # combine annotations
        polygons_old = to_polygons(self._annotations)
        polygons_new = to_polygons(element.annotations)
        matches = self._find_matches(polygons_old, polygons_new)
        combined = []
        for o, n, iou in matches:
            if o == -1:
                combined.append(element.annotations[n])
            elif n == -1:
                combined.append(self._annotations[o])
            else:
                # combine polygons
                if self.combination == UNION:
                    poly_comb = unary_union([polygons_new[n], polygons_old[o]])
                elif self.combination == INTERSECT:
                    poly_comb = polygons_new[n].intersection(polygons_old[o])
                else:
                    raise Exception("Unknown combination method: %s" % self.combination)
                # grab the first polygon
                if isinstance(poly_comb, GeometryCollection):
                    for x in poly_comb.geoms:
                        if isinstance(x, Polygon):
                            poly_comb = x
                            break
                elif isinstance(poly_comb, MultiPolygon):
                    for x in poly_comb.geoms:
                        if isinstance(x, Polygon):
                            poly_comb = x
                            break

                if isinstance(poly_comb, Polygon):
                    # create new located object
                    minx, miny, maxx, maxy = [int(x) for x in poly_comb.bounds]
                    x_list, y_list = poly_comb.exterior.coords.xy
                    points = []
                    for i in range(len(x_list)):
                        points.append(WaiPoint(x=x_list[i], y=y_list[i]))
                    lobj = LocatedObject(minx, miny, maxx - minx + 1, maxy - miny + 1)
                    lobj.set_polygon(WaiPolygon(*points))
                    lobj.metadata[STREAM_INDEX] = self._stream_index
                    combined.append(lobj)
                else:
                    self.logger.warning("Unhandled geometry type returned from combination, skipping: %s" % str(type(poly_comb)))

        self._annotations = LocatedObjects(combined)

        # new element
        then(element.__class__(element.data, self._annotations))
