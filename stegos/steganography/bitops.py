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


def clear_bit(byte_array: np.ndarray, bit_index: int) -> np.ndarray:
    """
    Clear bit values of a NumPy array.
    :param byte_array: NumPy array of bytes.
    :param bit_index: The index of the bits to clear.
    :return: NumPy array of bytes with the cleared bits.
    """
    mask = np.uint8(1 << bit_index)
    return byte_array & ~mask


def embed_bits_in_bytes(
    byte_array: np.ndarray, bit_array: np.ndarray, bit_index: int
) -> np.ndarray:
    """
    Embed bits in a NumPy array.
    :param byte_array: NumPy array of bytes to embed bits in.
    :param bit_array: NumPy array of bits to embed.
    :param bit_index: The index of the bits to replace.
    :return: NumPy array of bytes with the embedded bits.
    """
    byte_array = clear_bit(byte_array, bit_index)
    return byte_array | np.uint8(bit_array << bit_index)
