import csv
import json
import sys
from collections import OrderedDict
import termplotlib as tpl
import numpy as np

from wai.annotations.core.component import SinkComponent
from wai.annotations.domain.image import ImageInstance
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance

from wai.common.cli.options import TypedOption, FlagOption

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class AreaHistogram(
    SinkComponent[ImageInstance]
):

    label_key: str = TypedOption(
        "--label-key",
        type=str,
        default="type",
        help="the key in the meta-data that contains the label."
    )

    num_bins: int = TypedOption(
        "--num-bins",
        type=int,
        default=20,
        help="the number of bins to use for the histogram."
    )

    force_bbox: str = FlagOption(
        "-b", "--force-bbox",
        help="whether to use the bounding box even if a polygon is present (object detection domain only)"
    )

    normalized: bool = FlagOption(
        "-n", "--normalized",
        help="whether to use normalized areas (using the image size as base)."
    )

    all_label: str = TypedOption(
        "-a", "--all-label",
        type=str,
        default="ALL",
        help="the label to use for all the labels combined"
    )

    output_format: str = TypedOption(
        "-f", "--format",
        type=str,
        default=OUTPUT_FORMAT_TEXT,
        help="the format to use for the output, available modes: %s" % ", ".join(OUTPUT_FORMATS)
    )

    output_file: str = TypedOption(
        "-o", "--output",
        type=str,
        default="",
        help="the file to write the histogram to; uses stdout if omitted"
    )

    def init_labels(self):
        """
        Initializes the labels.
        """
        if not hasattr(self, "_data"):
            self._data = dict()

    def append_value(self, label, value):
        """
        Appends a value to the label.
        """
        self.init_labels()

        if "" not in self._data:
            self._data[""] = []
        if label not in self._data:
            self._data[label] = []

        if value <= 0:
            self.logger.warning("Invalid area (%s): %f" % (label, value))

        if label is not "":
            self._data[""].append(value)
        self._data[label].append(value)

    def create_all_label(self, labels):
        """
        Creates a unique label for "all".

        :param labels: the labels used in the dataset
        :type labels: list
        :return: the generated all label
        :rtype: str
        """
        result = self.all_label
        label_set = set(labels)
        while result in label_set:
            result = "_" + result + "_"
        return result

    def output_text(self, histograms, keys, use_stdout):
        """
        Outputs the label distribution in simple textual format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        plots = ""
        for k in keys:
            if k is "":
                label = self.create_all_label(keys)
            else:
                label = k
            plots += label + ":\n\n"
            counts, bin_edges = histograms[k]
            fig = tpl.figure()
            fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)
            plots += fig.get_string() + "\n\n"

        if use_stdout:
            print(plots)
        else:
            with open(self.output_file, "w") as fp:
                fp.write(plots)

    def output_csv(self, histograms, keys, use_stdout):
        """
        Outputs the label distribution in CSV format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(self.output_file, "w")
            writer = csv.writer(f)

        writer.writerow(["label", "bin", "from", "to", "count"])
        for k in keys:
            if k is "":
                label = self.create_all_label(keys)
            else:
                label = k
            counts, bin_edges = histograms[k]
            for i in range(len(counts)):
                writer.writerow([label, i, bin_edges[i], bin_edges[i+1], counts[i]])

        if f is not None:
            f.close()

    def output_json(self, histograms, keys, use_stdout):
        """
        Outputs the label distribution in json format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        data = []
        for k in keys:
            if k is "":
                label = self.create_all_label(keys)
            else:
                label = k
            counts, bin_edges = histograms[k]
            label_data = OrderedDict()
            label_data["label"] = label
            label_data["bins"] = []
            for i in range(len(counts)):
                bin = OrderedDict()
                bin["bin"] = i
                bin["from"] = float(bin_edges[i])
                bin["to"] = float(bin_edges[i+1])
                bin["count"] = int(counts[i])
                label_data["bins"].append(bin)
            data.append(label_data)

        if use_stdout:
            print(json.dumps(data, indent=2))
        else:
            with open(self.output_file, "w") as f:
                json.dump(data, f, indent=2)

    def output_histograms(self):
        """
        Computes and outputs the histograms.
        """
        histograms = dict()
        keys = []
        for k in self._data:
            if k is not "":
                keys.append(k)
            counts, bin_edges = np.histogram(self._data[k], bins=self.num_bins)
            histograms[k] = (counts, bin_edges)

        use_stdout = len(self.output_file) == 0

        keys.sort()
        keys.insert(0, "")

        if self.output_format == "text":
            self.output_text(histograms, keys, use_stdout)
        elif self.output_format == "csv":
            self.output_csv(histograms, keys, use_stdout)
        elif self.output_format == "json":
            self.output_json(histograms, keys, use_stdout)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def consume_element(self, element: ImageInstance):
        """
        Consumes instances by discarding them.
        """
        img_area = element.data.width * element.data.height
        if isinstance(element, ImageObjectDetectionInstance):
            for obj in element.annotations:
                label = ""
                if self.label_key in obj.metadata:
                    label = obj.metadata[self.label_key]
                if not self.force_bbox and obj.has_polygon():
                    area = obj.get_polygon().area()
                else:
                    area = obj.get_rectangle().area()
                if self.normalized:
                    self.append_value(label, area / img_area)
                else:
                    self.append_value(label, area)
        elif isinstance(element, ImageSegmentationInstance):
            label_images = element.annotations.label_images
            for label in label_images:
                area = np.count_nonzero(label_images[label])
                if self.normalized:
                    self.append_value(label, area / img_area)
                else:
                    self.append_value(label, area)

    def finish(self):
        self.init_labels()
        self.output_histograms()
