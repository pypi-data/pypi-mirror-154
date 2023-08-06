Changelog
=========

1.0.3 (2022-06-13)
------------------

- added `combine-annotations-od` for combining overlapping annotations between images into single annotation
- `add-annotation-overlay-is/od` now use `narg='+'` for `--labels` and `--colors` options instead of comma-separated single argument


1.0.2 (2022-05-11)
------------------

- making use of the new Image segmentation annotations property `label_images` to get
  separate images for generating overlays with `AnnotationOverlayIS`


1.0.1 (2022-05-10)
------------------

- add-annotation-overlay-ic now can draw a filled background rectangle for the label
  for better readability


1.0.0 (2022-05-09)
------------------

- Initial release: add-annotation-overlay-(ic/is/od), image-viewer-(ic/is/od)
- Received to-annotation-overlay-od from wai.annotations.imgstats

