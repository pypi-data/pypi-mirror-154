# wai-annotations-imgstats
wai.annotations plugin for generating statistics for image datasets.

## Plugins
### AREA-HISTOGRAM-IS
Generates histograms of the area (normalized or absolute) occupied by the annotations.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: area-histogram-is [-a ALL_LABEL] [-b] [--label-key LABEL_KEY] [-n] [--num-bins NUM_BINS] [-o OUTPUT_FILE] [-f OUTPUT_FORMAT]

optional arguments:
  -a ALL_LABEL, --all-label ALL_LABEL
                        the label to use for all the labels combined
  -b, --force-bbox      whether to use the bounding box even if a polygon is present (object detection domain only)
  --label-key LABEL_KEY
                        the key in the meta-data that contains the label.
  -n, --normalized      whether to use normalized areas (using the image size as base).
  --num-bins NUM_BINS   the number of bins to use for the histogram.
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the histogram to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
```

### AREA-HISTOGRAM-OD
Generates histograms of the area (normalized or absolute) occupied by the annotations.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: area-histogram-od [-a ALL_LABEL] [-b] [--label-key LABEL_KEY] [-n] [--num-bins NUM_BINS] [-o OUTPUT_FILE] [-f OUTPUT_FORMAT]

optional arguments:
  -a ALL_LABEL, --all-label ALL_LABEL
                        the label to use for all the labels combined
  -b, --force-bbox      whether to use the bounding box even if a polygon is present (object detection domain only)
  --label-key LABEL_KEY
                        the key in the meta-data that contains the label.
  -n, --normalized      whether to use normalized areas (using the image size as base).
  --num-bins NUM_BINS   the number of bins to use for the histogram.
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the histogram to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
```

### LABEL-DIST-IC
Generates a label distribution.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: label-dist-ic [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```

### LABEL-DIST-IS
Generates a label distribution.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: label-dist-is [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```

### LABEL-DIST-OD
Generates a label distribution.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: label-dist-od [--label-key LABEL_KEY] [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-p]

optional arguments:
  --label-key LABEL_KEY
                        the key in the meta-data that contains the label.
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write the statistics to; uses stdout if omitted
  -f OUTPUT_FORMAT, --format OUTPUT_FORMAT
                        the format to use for the output, available modes: csv, json
  -p, --percentages     whether to output percentages instead of counts.
```
