from stegos.steganography import bitops
from stegos.steganography.exception import (
    InsufficientCapacityException,
    InvalidCoverImageException,
)

import numpy as np

from stegos.steganography.base import SeededSteganography


class LSBSteganography(SeededSteganography):
    """LSB steganography algorithm that embeds directly in an image's pixels.

    This algorithm should only be used for lossless file formats. Otherwise, embedded data may be lost during lossy compression.
    """

    PAYLOAD_SIZE_BYTES = 4

    def __init__(self, seed: int, lsb_depth: int = 2):
        super().__init__(seed, lsb_depth)

    def _payload_capacity(self, cover_image):
        capacity = len(cover_image) - self.PAYLOAD_SIZE_BYTES * 8
        capacity *= self.lsb_depth
        return capacity // 8

    def embed(self, cover_image, payload):
        payload_size = len(payload)
        if payload_size == 0:
            raise ValueError("payload must not be empty")

        pixels: np.ndarray = cover_image.ravel()

        payload_capacity = self._payload_capacity(pixels)
        if payload_capacity <= 0:
            raise InvalidCoverImageException(
                f"cover image capacity insufficient to store payload header of {self.PAYLOAD_SIZE_BYTES} bytes"
            )
        elif payload_capacity < payload_size:
            raise InsufficientCapacityException(payload_size, payload_capacity)

        random_indices = self._random_indices(pixels)

        payload_bits = bitops.bytes_to_bits(payload)
        size_bits = bitops.int_to_bits(len(payload_bits), self.PAYLOAD_SIZE_BYTES)
        payload_bits = np.concatenate([size_bits, bitops.bytes_to_bits(payload)])

        bits_written = 0
        for bit_index in range(self.lsb_depth):
            if bits_written >= len(payload_bits):
                break

            remaining = len(payload_bits) - bits_written
            bits_to_write = min(len(random_indices), remaining)

            write_indices = random_indices[:bits_to_write]
            pixels[write_indices] = bitops.embed_bits(
                pixels[write_indices],
                payload_bits[bits_written : bits_written + bits_to_write],
                bit_index,
            )

            bits_written += bits_to_write

        return pixels.reshape(cover_image.shape)

    def extract(self, stego_image):
        pixels: np.ndarray = stego_image.ravel()
        random_indices = self._random_indices(pixels)

        payload_size_bits = self.PAYLOAD_SIZE_BYTES * 8
        size_bits = bitops.get_bit(
            pixels[random_indices[:payload_size_bits]], bit_index=0
        )
        payload_size = bitops.bits_to_int(size_bits)

        bits_read = 0
        payload = np.empty(payload_size_bits + payload_size, dtype=np.uint8)
        for bit_pos in range(self.lsb_depth):
            if bits_read >= payload_size:
                break

            remaining = payload_size - bits_read
            bits_to_read = min(pixels.size, remaining)

            read_indices = random_indices[:bits_to_read]
            bits = bitops.get_bit(pixels[read_indices], bit_pos)

            payload[bits_read : bits_read + bits_to_read] = bits
            bits_read += bits_to_read

        return bitops.bits_to_bytes(payload[payload_size_bits:])
