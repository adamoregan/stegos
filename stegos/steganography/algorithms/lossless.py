from stegos.steganography import bitops
from stegos.steganography.exception import UnsupportedColorSpaceError

import numpy as np
from numpy.random import default_rng

from stegos.steganography.base import SeededSteganographyStrategy


class LosslessSteganographyStrategy(SeededSteganographyStrategy):
    """Class defining a lossless steganography algorithm that embeds directly in an image's pixels.

    This algorithm should only be used for lossless file formats. Otherwise, the embedded data may be lost during lossy compression.
    """

    PAYLOAD_SIZE_BYTES = 4

    def payload_capacity(self, cover_image):
        match cover_image.ndim:
            case 2:
                height, width = cover_image.shape
                capacity = height * width
            case 3:
                height, width, bands = cover_image.shape
                capacity = height * width * bands
            case _:
                raise UnsupportedColorSpaceError(
                    f"image with {cover_image.ndim} dimensions not supported."
                )
        capacity = capacity - self.PAYLOAD_SIZE_BYTES * 8
        capacity *= self.lsb_depth
        return max(0, capacity // 8)

    def _random_indices(self, pixels: np.ndarray) -> np.ndarray:
        """
        Generates random indices for a NumPy array.
        :param pixels: NumPy array to generate random indices for.
        :return: NumPy array of randomised indices.
        """
        rng = np.random.default_rng(self.seed)  # stateful
        return rng.choice(pixels.size, pixels.size, replace=False)

    def embed(self, cover_image, payload):
        pixels: np.ndarray = cover_image.ravel()
        random_indices = self._random_indices(pixels)

        payload_bits = bitops.bytes_to_bits(payload)
        size_bits = bitops.int_to_bits(len(payload_bits), self.PAYLOAD_SIZE_BYTES)
        header_indices = random_indices[: len(size_bits)]
        pixels[header_indices] = bitops.embed_bits_in_bytes(
            pixels[header_indices],
            size_bits,
            bit_index=0,
        )

        payload_indices = random_indices[len(size_bits) :]

        bits_written = 0
        for bit_pos in range(self.lsb_depth):
            if bits_written >= len(payload_bits):
                break

            remaining = len(payload_bits) - bits_written
            bits_to_write = min(len(payload_indices), remaining)

            write_indices = payload_indices[:bits_to_write]
            pixels[write_indices] = bitops.embed_bits_in_bytes(
                pixels[write_indices],
                payload_bits[bits_written : bits_written + bits_to_write],
                bit_pos,
            )

            bits_written += bits_to_write

        return pixels.reshape(cover_image.shape)

    def extract(self, stego_image):
        pixels: np.ndarray = stego_image.ravel()
        random_indices = self._random_indices(pixels)

        # Extract payload size
        payload_size_bits = self.PAYLOAD_SIZE_BYTES * 8
        size_bits = bitops.get_bit(
            pixels[random_indices[:payload_size_bits]], bit_index=0
        )
        payload_size = bitops.bits_to_int(size_bits)

        payload_indices = random_indices[payload_size_bits:]
        payload_bits = np.empty(payload_size, dtype=np.uint8)

        bits_read = 0
        for bit_pos in range(self.lsb_depth):
            if bits_read >= payload_size:
                break

            remaining = payload_size - bits_read
            bits_to_read = min(len(payload_indices), remaining)

            read_indices = payload_indices[:bits_to_read]
            bits = bitops.get_bit(pixels[read_indices], bit_pos)

            payload_bits[bits_read : bits_read + bits_to_read] = bits
            bits_read += bits_to_read

        return bitops.bits_to_bytes(payload_bits)
