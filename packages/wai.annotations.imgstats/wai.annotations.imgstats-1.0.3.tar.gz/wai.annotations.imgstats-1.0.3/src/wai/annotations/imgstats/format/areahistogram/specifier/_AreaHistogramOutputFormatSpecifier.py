from abc import ABC
from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.specifier import SinkStageSpecifier


class AreaHistogramOutputFormatSpecifier(SinkStageSpecifier, ABC):
    """
    Base specifier for the area-histogram in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Generates histograms of the area (normalized or absolute) occupied by the annotations."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.imgstats.format.areahistogram.component import AreaHistogram
        return AreaHistogram,
