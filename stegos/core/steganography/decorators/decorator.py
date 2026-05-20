import numpy as np

from stegos.core.steganography.base import BaseLSBSteganography


class BaseLSBSteganographyDecorator(BaseLSBSteganography):
    """Decorator for BaseLSBSteganography objects."""

    def __init__(self, strategy: BaseLSBSteganography):
        """
        Creates an instance of BaseLSBSteganographyDecorator.
        :param strategy: Strategy to decorate.
        """
        super().__init__(strategy.lsb_depth)
        self._strategy = strategy

    @property
    def strategy(self) -> BaseLSBSteganography:
        """Gets the decorated strategy."""
        return self._strategy

    def embed(self, cover_image: np.ndarray, payload: bytes):
        self.strategy.embed(cover_image, payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        return self.strategy.extract(stego_image)
