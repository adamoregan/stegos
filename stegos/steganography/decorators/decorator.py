import numpy as np

from stegos.steganography.base import ImageSteganographyStrategy


class ImageSteganographyDecorator(ImageSteganographyStrategy):
    """Decorator for ImageSteganographyStrategy objects."""

    def __init__(self, strategy: ImageSteganographyStrategy):
        super().__init__(strategy.lsb_depth)
        self._strategy = strategy

    @property
    def strategy(self) -> ImageSteganographyStrategy:
        return self._strategy

    def payload_capacity(self, cover_image: np.ndarray) -> int:
        return self.strategy.payload_capacity(cover_image)

    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        return self.strategy.embed(cover_image, payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        return self.strategy.extract(stego_image)
