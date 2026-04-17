import io
import lzma
import zipfile
from typing import Iterable, Generator

import jpegio as jio
import numpy as np
from PIL import Image

from stegos.core.compression.file import FileCompressor, ZipCompressor
from stegos.core.constants import (
    get_compression_type,
    ImageCompressionType,
    MixedFormat,
)
from stegos.core.exception import UnsupportedImageFormatException
from stegos.core.steganography.algorithms.lossy import LossyLSBSteganography
from stegos.core.steganography.algorithms.lsb import LSBSteganography
from stegos.core.steganography.decorators.encryption import EncryptionDecorator


class LSBSteganographyService:
    """Service/facade for LSB steganography operations.

    Coordinates compression, encryption + key derivation, and steganography operations for files and arbitrary bytes.
    """

    def __init__(self, file_compressor: FileCompressor = None):
        """
        Creates an instance of LSBSteganographyService.
        :param file_compressor: Compressor used to compress and decompress hidden files.
        """
        self._file_compressor = file_compressor or ZipCompressor()

    @staticmethod
    def _get_strategy(
        compression_type: ImageCompressionType, image: Image.Image, password: bytes
    ) -> EncryptionDecorator:
        """
        Gets the appropriate image steganography strategy.
        :param compression_type: Compression type of the image.
        :param image: Image used as a cover image or stego image.
        :param password: Password used to encrypt the payload.
        :return: Image steganography strategy configured based on compression type.
        """
        strategy = LSBSteganography(1)
        match compression_type:
            case ImageCompressionType.LOSSY:
                strategy = LossyLSBSteganography(1)
            case ImageCompressionType.MIXED:
                if MixedFormat.type(image) == ImageCompressionType.LOSSY:
                    raise UnsupportedImageFormatException(
                        "mixed image formats with lossy compression are unsupported"
                    )
        return EncryptionDecorator(strategy, password)

    def _compress_payload(self, payload) -> bytes:
        """
        Compresses a payload.
        :param payload: Payload to compress.
        :return: Payload as bytes.
        """
        if isinstance(payload, bytes):
            return lzma.compress(payload)
        return self._file_compressor.compress(payload)

    def embed(
        self, cover_image: str, payload: bytes | Iterable[str], password: bytes
    ) -> Image.Image | jio.DecompressedJpeg:
        """
        Embeds a payload into an image.

        Compresses and encrypts the payload before embedding it.
        :param cover_image: Cover image used as the carrier of the payload.
        :param payload: Payload to embed inside the cover image. Should be bytes or a list of file paths.
        :param password: Password used to encrypt the payload. A key is derived from the password.
        :return:
        """
        image = Image.open(cover_image)
        compression_type = get_compression_type(image)
        strategy = LSBSteganographyService._get_strategy(
            compression_type, image, password
        )
        compressed = self._compress_payload(payload)
        if compression_type == ImageCompressionType.LOSSY:
            image = jio.read(cover_image)
            strategy.embed(image.coef_arrays[0], compressed)
            return image
        img_arr = np.array(image)
        strategy.embed(img_arr, compressed)
        return Image.fromarray(img_arr)

    def extract(
        self, stego_image: str, password: bytes
    ) -> Generator[tuple[str, bytes], None, None]:
        """
        Extracts a payload from an image.

        :param stego_image: Stego image that contains a hidden payload.
        :param password: Password used to decrypt the payload. A key is derived from the password.
        :return: If the payload is an archive, returns the names and contents of each file. Otherwise, returns "output"
        and the embedded bytes.
        """
        image = Image.open(stego_image)
        compression_type = get_compression_type(image)
        strategy = LSBSteganographyService._get_strategy(
            compression_type, image, password
        )
        if compression_type == ImageCompressionType.LOSSY:
            image = jio.read(stego_image).coef_arrays[0]
        extracted = strategy.extract(np.array(image))
        if zipfile.is_zipfile(io.BytesIO(extracted)):
            for name, content in self._file_compressor.decompress(extracted):
                yield name, content
        else:
            yield "output", lzma.decompress(extracted)
