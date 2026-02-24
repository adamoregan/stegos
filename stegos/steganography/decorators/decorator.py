import numpy as np

from stegos.steganography.base import BaseLSBSteganography


class BaseLSBSteganographyDecorator(BaseLSBSteganography):
    """Decorator for BaseLSBSteganography objects."""

    def __init__(self, strategy: BaseLSBSteganography):
        super().__init__(strategy.lsb_depth)
        self._strategy = strategy

    @property
    def strategy(self) -> BaseLSBSteganography:
        return self._strategy

    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        return self.strategy.embed(cover_image, payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        return self.strategy.extract(stego_image)
