"""This module provides functions to manipulate bit values."""

import numpy as np


def bytes_to_bits(data: bytes) -> np.ndarray:
    """
    Convert bytes into a NumPy array of bits.
    :param data: Byte data.
    :return: Numpy array of bits.
    """
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))


def bits_to_bytes(bits: np.ndarray) -> bytes:
    """
    Convert a NumPy array of bits to bytes.
    :param bits: NumPy array of bits.
    :return: Byte data.
    """
    if len(bits) == 0:
        return b""
    packed: np.ndarray = np.packbits(bits)
    return packed.tobytes()


def int_to_bits(num: int, length: int) -> np.ndarray:
    """
    Convert a number to a NumPy array of bits.
    :param num: Integer to convert.
    :param length: Length of bytes to use.
    :return: NumPy array of bits representing the integer.
    """
    return bytes_to_bits(num.to_bytes(length, byteorder="big"))


def bits_to_int(bits: np.ndarray) -> int:
    """
    Convert NumPy array of bits to an integer.
    :param bits: NumPy array of bits.
    :return: Integer representing the NumPy array of bits.
    """
    return int.from_bytes(bits_to_bytes(bits), byteorder="big")


def get_bit(byte_array: np.ndarray, bit_index: int = 0) -> np.ndarray:
    """
    Gets bit values of a NumPy array.
    :param byte_array: NumPy array of bytes.
    :param bit_index: The position of the bits to retrieve.
    :return: NumPy array of retrieved bits.
    """
    return (byte_array >> bit_index) & 1


def clear_bit(carrier_array: np.ndarray, bit_index: int) -> np.ndarray:
    """
    Clear bit values of a NumPy array.
    :param carrier_array: NumPy array of bytes.
    :param bit_index: The index of the bits to clear.
    :return: NumPy array of bytes with the cleared bits.
    """
    mask = np.array(1 << bit_index, dtype=carrier_array.dtype)
    return carrier_array & ~mask


def embed_bits(
    carrier_array: np.ndarray, bit_array: np.ndarray, bit_index: int
) -> np.ndarray:
    """
    Embed bits in a NumPy array.
    :param carrier_array: NumPy integer array to embed bits in.
    :param bit_array: NumPy array of bits to embed.
    :param bit_index: The index of the bits to replace.
    :return: NumPy array of integers with the embedded bits.
    """
    carrier_array = clear_bit(carrier_array, bit_index)
    return carrier_array | bit_array << bit_index


def has_msb_set(bits: np.ndarray, lsb_depth: int) -> np.ndarray:
    """
    Checks if bits are set.
    :param bits: Bits to check.
    :param lsb_depth: Number of LSBs to ignore.
    :return: NumPy array of booleans indicating where the MSBs are set.
    """
    return np.any(bits[:, :-lsb_depth] == 1, axis=1)


def int32_to_bits(nums: np.ndarray) -> np.ndarray:
    """
    Converts int32 integers to their bit representations.
    :param nums: Integers to convert.
    :return: NumPy array of bits representing the integers.
    """
    return np.unpackbits(nums.astype(">i4").view(np.uint8)).reshape(-1, 32)
