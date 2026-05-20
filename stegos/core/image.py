from abc import abstractmethod
from pathlib import Path
from typing import Protocol

import jpegio as jio


class Image(Protocol):
    """Image for steganography operations."""

    @abstractmethod
    def save(self, path: str | Path) -> None:
        """
        Saves the image.
        :param path: Filename to save the image as.
        """
        pass


class JPEGImage(Image):
    """JPEG image for DCT steganography operations."""

    def __init__(self, image: jio.DecompressedJpeg):
        """
        Creates an instance of JPEGImage.
        :param image: Image opened with jpegio.
        """
        self._image = image

    def save(self, path: str | Path) -> None:
        jio.write(self._image, path)
