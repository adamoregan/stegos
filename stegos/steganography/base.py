from abc import ABC, abstractmethod
import numpy as np

from stegos.steganography.exception import InsufficientCapacityException


class ImageSteganographyStrategy(ABC):
    """Abstract class defining an image steganography algorithm."""

    def __init__(self, lsb_depth: int = 2):
        """
        Creates an instance of the ImageSteganographyStrategy class.
        :param lsb_depth: The least significant bit embedding depth of the algorithm.
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
    def payload_capacity(self, cover_image: np.ndarray) -> int:
        """
        Calculates the available capacity for the payload in bytes.
        :param cover_image: Image used as the carrier for hidden data.
        :return: Maximum payload size in bytes.
        """
        pass

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


class SeededSteganographyStrategy(ImageSteganographyStrategy, ABC):
    """Abstract base class defining a seeded image steganography algorithm."""

    def __init__(self, seed: int, lsb_depth: int = 2):
        """
        Creates an instance of the SeededSteganographyStrategy class.
        :param seed: Seed controlling algorithm randomness.
        :param lsb_depth: The least significant bit embedding depth of the algorithm.
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


class ImageSteganographyContext:
    """Context class for image steganography."""

    def __init__(self, strategy: ImageSteganographyStrategy):
        """
        Creates an instance of the ImageSteganographyContext class.
        :param strategy: Strategy used to perform image steganography.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> ImageSteganographyStrategy:
        """
        Gets the strategy used to perform image steganography.
        :return: The current image steganography algorithm.
        """
        return self._strategy

    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        """
        Embed a payload into a cover image.
        :param cover_image: Image used as the carrier for hidden data.
        :param payload: Binary data to hide in the cover image.
        :return: Stego image containing the embedded payload.
        """
        payload_size = len(payload)
        if payload_size == 0:
            raise ValueError("payload must not be empty")

        payload_capacity = self.strategy.payload_capacity(cover_image)
        if payload_size > payload_capacity:
            raise InsufficientCapacityException(payload_size, payload_capacity)

        return self.strategy.embed(cover_image, payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        """
        Extract a payload from a stego image.
        :param stego_image: Image used as the carrier for hidden data.
        :return: Extracted payload as bytes.
        """
        return self.strategy.extract(stego_image)
