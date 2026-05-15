import secrets

import numpy as np

from stegos.core.steganography import bitops
from stegos.core.steganography.bitops import BITS_PER_BYTE
from stegos.core.steganography.exception import (
    InsufficientCapacityException,
    InvalidCoverImageException,
)
from stegos.core.steganography.base import SeededSteganography


class LSBSteganography(SeededSteganography):
    """LSB steganography algorithm that embeds directly in an image's pixels.

    This algorithm should only be used for lossless file formats. Otherwise, embedded data may be lost during lossy compression.
    """

    PAYLOAD_SIZE_BYTES = 4

    def __init__(self, lsb_depth: int = 2):
        super().__init__(lsb_depth)

    def _payload_capacity(self, cover_image):
        capacity = len(cover_image) - (self.PAYLOAD_SIZE_BYTES * BITS_PER_BYTE)
        capacity -= self.SEED_SIZE_BYTES * BITS_PER_BYTE
        capacity *= self.lsb_depth
        return capacity // 8

    def _validate_capacity(self, capacity: int, payload_size: int):
        """
        Validates image capacity to ensure the payload can be embedded.
        :param capacity: Image capacity.
        :param payload_size: Size of the payload in bytes
        """
        if capacity <= 0:
            raise InvalidCoverImageException(
                f"cover image capacity insufficient to store payload header of {self.PAYLOAD_SIZE_BYTES} bytes"
            )
        elif capacity < payload_size:
            raise InsufficientCapacityException(payload_size, capacity)

    def embed(self, cover_image, payload):
        payload_size = len(payload)
        if payload_size == 0:
            raise ValueError("payload must not be empty")

        pixels: np.ndarray = cover_image.ravel()

        payload_capacity = self._payload_capacity(pixels)
        self._validate_capacity(payload_capacity, payload_size)

        self._seed = secrets.randbits(self.SEED_SIZE_BYTES * BITS_PER_BYTE)
        seed_bits = bitops.int_to_bits(self._seed, self.SEED_SIZE_BYTES)
        pixels[: len(seed_bits)] = bitops.embed_bits(
            pixels[: len(seed_bits)], seed_bits, 0
        )

        random_indices = self._random_indices(pixels)
        random_indices = random_indices[random_indices >= len(seed_bits)]

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

    def extract(self, stego_image):
        pixels: np.ndarray = stego_image.ravel()

        seed_bits = bitops.get_bit(pixels[: self.SEED_SIZE_BYTES * BITS_PER_BYTE])
        self._seed = bitops.bits_to_int(seed_bits)
        random_indices = self._random_indices(pixels)
        random_indices = random_indices[random_indices >= len(seed_bits)]

        payload_size_bits = self.PAYLOAD_SIZE_BYTES * BITS_PER_BYTE
        size_bits = bitops.get_bit(
            pixels[random_indices[:payload_size_bits]], bit_index=0
        )
        payload_size = bitops.bits_to_int(size_bits)

        bits_read = 0
        payload = np.empty(payload_size_bits + payload_size, dtype=np.uint8)
        for bit_index in range(self.lsb_depth):
            if bits_read >= payload_size:
                break

            remaining = len(payload) - bits_read
            bits_to_read = min(len(random_indices), remaining)

            read_indices = random_indices[:bits_to_read]
            bits = bitops.get_bit(pixels[read_indices], bit_index)

            payload[bits_read : bits_read + bits_to_read] = bits
            bits_read += bits_to_read

        return bitops.bits_to_bytes(payload[payload_size_bits:])
