import numpy as np

from stegos.steganography.base import BaseLSBSteganography


class Dummy(BaseLSBSteganography):
    def __init__(self, lsb_depth: int = 2):
        super().__init__(lsb_depth)
        self._payload = None

    def embed(self, cover_image, payload):
        self._payload = payload
        return cover_image

    def extract(self, stego_image):
        return self._payload


def create_image(width=8, height=8, mode="RGB") -> np.ndarray:
    """
    Creates a sample image.
    :param width: The width of the image
    :param height: The height of the image.
    :param mode: The mode of the image.
    :return: NumPy array representing an image.
    """
    rng = np.random.default_rng(seed=1)
    if mode == "L":
        data = rng.integers(0, 256, size=(height, width), dtype=np.uint8)
    else:
        data = rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)
    return data
