from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class CombineAnnotationsODISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the combine-annotations object detection ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Combines object detection annotations from images passing through into a single annotation."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"CombineAnnotationsOD only handles the following domains: "
                f"{ImageObjectDetectionDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.imgvis.isp.combine_annotations.component import CombineAnnotationsOD
        return CombineAnnotationsOD,
