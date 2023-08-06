from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._AreaHistogramOutputFormatSpecifier import AreaHistogramOutputFormatSpecifier


class AreaHistogramODOutputFormatSpecifier(AreaHistogramOutputFormatSpecifier):
    """
    Specifier for area-histogram in the object-detection domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
