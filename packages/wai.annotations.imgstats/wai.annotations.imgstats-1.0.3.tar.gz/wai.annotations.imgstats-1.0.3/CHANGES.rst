Changelog
=========

1.0.3 (2022-06-13)
------------------

- `label-dist-od` now has `--label-key` option to specify the meta-data key that stores the label
- `label-dist-XY` now sort the labels in alphabetically order before outputting the statistics
- added `area-histogram-is` and `area-histogram-od`


1.0.2 (2022-05-09)
------------------

- moved `to-annotation-overlay-od` into `wai.annotations.imgvis` module


1.0.1 (2022-05-04)
------------------

- added `-s/--scale-to` option to `to-annotation-overlay-od` command to scale all annotations
  to a predefined image size.
- overlay output of `to-annotation-overlay-od` is now enforcing PNG format


1.0.0 (2022-05-02)
------------------

- Initial release: label-dist-ic, label-dist-is, label-dist-od, to-annotation-overlay-od

