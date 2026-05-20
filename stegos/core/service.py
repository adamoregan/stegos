import io
import lzma
import zipfile
from dataclasses import dataclass
from typing import Iterable, Generator

import jpegio as jio
import numpy as np
from PIL import Image as PILImage

from stegos.core.compression.file import FileCompressor, ZipCompressor
from stegos.core.constants import (
    compression_type,
    ImageCompressionType,
)
from stegos.core.image import JPEGImage, Image
from stegos.core.steganography.builder import SteganographyStrategyBuilder


@dataclass
class ExtractedItem:
    """Item extracted from an image."""

    content: bytes
    is_file: bytes
    name: str = None


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
    ) -> Image:
        """
        Embeds a payload into an image.

        Compresses and encrypts the payload before embedding it.
        :param cover_image: Cover image used as the carrier of the payload.
        :param payload: Payload to embed inside the cover image. Should be bytes or a list of file paths.
        :param password: Password used to encrypt the payload. A key is derived from the password.
        :return: Image with the embedded payload.
        """
        image = PILImage.open(cover_image)
        comp_type = compression_type(image)
        strategy = (
            SteganographyStrategyBuilder(comp_type, image).encryption(password).build()
        )
        compressed = self._compress_payload(payload)
        if comp_type == ImageCompressionType.LOSSY:
            image = jio.read(cover_image)
            strategy.embed(image.coef_arrays[0], compressed)
            return JPEGImage(image)
        img_arr = np.array(image)
        strategy.embed(img_arr, compressed)
        return PILImage.fromarray(img_arr)

    def extract(
        self, stego_image: str, password: bytes
    ) -> Generator[ExtractedItem, None, None]:
        """
        Extracts a payload from an image.

        :param stego_image: Stego image that contains a hidden payload.
        :param password: Password used to decrypt the payload. A key is derived from the password.
        :return: Yields extracted items which can be files or bytes.
        """
        image = PILImage.open(stego_image)
        comp_type = compression_type(image)
        strategy = (
            SteganographyStrategyBuilder(comp_type, image).encryption(password).build()
        )
        if comp_type == ImageCompressionType.LOSSY:
            image = jio.read(stego_image).coef_arrays[0]
        extracted = strategy.extract(np.array(image))
        if zipfile.is_zipfile(io.BytesIO(extracted)):
            for name, content in self._file_compressor.decompress(extracted):
                yield ExtractedItem(content, is_file=True, name=name)
        else:
            yield ExtractedItem(lzma.decompress(extracted), is_file=False)
