from enum import StrEnum, auto

from PIL import Image


class ImageCompressionType(StrEnum):
    """Image compression types."""

    LOSSLESS = auto()
    LOSSY = auto()
    MIXED = auto()


class LossyFormat(StrEnum):
    """Images formats with lossy compression."""

    JPEG = auto()
    JPG = auto()


class MixedFormat(StrEnum):
    """Image formats with lossless or lossy compression."""

    TIFF = auto()
    WEBP = auto()

    @staticmethod
    def type(image: Image) -> ImageCompressionType:
        """
        Gets the compression type of a mixed format image.
        :param image: Mixed format image.
        :return: Compression type of the mixed format image.
        """
        compression = image.info.get("compression", "")
        if LossyFormat.JPEG in compression:
            return ImageCompressionType.LOSSY
        return ImageCompressionType.LOSSLESS


def get_compression_type(image: Image) -> ImageCompressionType:
    """
    Gets the compression type of an image.
    :param image: Image to get the compression type of.
    :return: Compression type of the image.
    """
    frmt = image.format.lower()
    if frmt in LossyFormat:
        return ImageCompressionType.LOSSY
    elif frmt in MixedFormat:
        return ImageCompressionType.MIXED
    return ImageCompressionType.LOSSLESS
