from PIL.Image import Image

from stegos.core.constants import ImageCompressionType, MixedFormat
from stegos.core.exception import UnsupportedImageFormatException
from stegos.core.steganography.algorithms.lossy import LossyLSBSteganography
from stegos.core.steganography.algorithms.lsb import LSBSteganography
from stegos.core.steganography.base import BaseLSBSteganography
from stegos.core.steganography.decorators.encryption import EncryptionDecorator


def _get_base_strategy(
    compression_type: ImageCompressionType, image: Image
) -> BaseLSBSteganography:
    """
    Gets the appropriate image steganography strategy.
    :param compression_type: Compression type of the image.
    :param image: Image used as a cover image or stego image.
    :return: Image steganography strategy configured based on compression type.
    """
    match compression_type:
        case ImageCompressionType.LOSSY:
            return LossyLSBSteganography()
        case ImageCompressionType.MIXED:
            if MixedFormat.type(image) == ImageCompressionType.LOSSY:
                raise UnsupportedImageFormatException(
                    "mixed image formats with lossy compression are unsupported"
                )
    return LSBSteganography()


class SteganographyStrategyBuilder:
    def __init__(self, compression_type: ImageCompressionType, image: Image):
        self._strategy: BaseLSBSteganography = _get_base_strategy(
            compression_type, image
        )

    def encryption(self, password: bytes) -> "SteganographyStrategyBuilder":
        """
        Add encryption to the strategy.
        :param password: Password to derive a key from for encryption.
        :return: The builder instance.
        """
        self._strategy = EncryptionDecorator(self._strategy, password)
        return self

    def build(self) -> BaseLSBSteganography:
        """Gets the created strategy."""
        return self._strategy
