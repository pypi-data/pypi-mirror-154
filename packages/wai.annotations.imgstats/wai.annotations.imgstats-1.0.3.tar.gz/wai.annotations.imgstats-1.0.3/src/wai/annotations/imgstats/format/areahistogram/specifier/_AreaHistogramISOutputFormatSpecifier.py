from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._AreaHistogramOutputFormatSpecifier import AreaHistogramOutputFormatSpecifier


class AreaHistogramISOutputFormatSpecifier(AreaHistogramOutputFormatSpecifier):
    """
    Specifier for area-histogram in the image segmentation domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
