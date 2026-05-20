from abc import abstractmethod
from pathlib import Path
from typing import Protocol

import jpegio as jio


class Image(Protocol):
    @abstractmethod
    def save(self, path: str | Path) -> None:
        pass


class JPEGImage(Image):
    def __init__(self, image: jio.DecompressedJpeg):
        self._image = image

    def save(self, path: str | Path) -> None:
        jio.write(self._image, path)
