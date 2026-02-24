from abc import ABC, abstractmethod
import numpy as np


class BaseLSBSteganography(ABC):
    """Abstract class defining an image steganography algorithm."""

    def __init__(self, lsb_depth: int):
        """
        Creates an instance of the BaseLSBSteganography class.
        :param lsb_depth: Least significant bit embedding depth of the algorithm.
        """
        if not isinstance(lsb_depth, int):
            raise TypeError(f"lsb_depth must be an int, not {type(lsb_depth).__name__}")
        if not (1 <= lsb_depth <= 7):
            raise ValueError(f"invalid lsb_depth (expected 1 to 7, got {lsb_depth})")
        self._lsb_depth = lsb_depth

    @property
    def lsb_depth(self) -> int:
        """
        Gets the least significant bit embedding depth of the algorithm.
        :return: LSB depth value.
        """
        return self._lsb_depth

    @abstractmethod
    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        """
        Embed a payload into a cover image.
        :param cover_image: Image used as the carrier for hidden data.
        :param payload: Binary data to hide in the cover image.
        :return: Stego image containing the embedded payload.
        """
        pass

    @abstractmethod
    def extract(self, stego_image: np.ndarray) -> bytes:
        """
        Extract a payload from a stego image.
        :param stego_image: Image used as the carrier for hidden data.
        :return: Extracted payload as bytes.
        """
        pass


class SeededSteganography(BaseLSBSteganography, ABC):
    """Abstract base class defining a seeded LSB image steganography algorithm."""

    def __init__(self, seed: int, lsb_depth: int):
        """
        Creates an instance of the SeededSteganography class.
        :param seed: Seed controlling algorithm randomness.
        :param lsb_depth: Least significant bit embedding depth of the algorithm.
        """
        super().__init__(lsb_depth)
        if not isinstance(seed, int):
            raise TypeError(f"seed must be an int, not {type(seed).__name__}")
        self._seed = seed

    @property
    def seed(self) -> int:
        """
        Gets the seed controlling algorithm randomness.
        :return: Seed value.
        """
        return self._seed

    def _random_indices(self, pixels: np.ndarray) -> np.ndarray:
        """
        Generates random indices for a NumPy array.
        :param pixels: NumPy array to generate random indices for.
        :return: NumPy array of randomised indices.
        """
        rng = np.random.default_rng(self.seed)  # stateful
        return rng.choice(pixels.size, pixels.size, replace=False)
