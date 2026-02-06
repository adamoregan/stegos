import numpy as np
import pytest

from stegos.steganography import bitops


class TestBitops:
    """Tests for bitops.py."""

    @pytest.mark.parametrize(
        ("bytes_to_convert", "expected_bits"),
        [
            (b"\xff\xff\xff\xff", np.ones(32, dtype=np.uint8)),
            (b"\x00\x00\x00\x00", np.zeros(32, dtype=np.uint8)),
            (b"\x80\x00\x00\x00", np.array([1] + [0] * 31, dtype=np.uint8)),
            (b"\xff", np.ones(8, dtype=np.uint8)),
            (b"", np.empty(0)),
        ],
    )
    def test_bytes_to_bits(self, bytes_to_convert: bytes, expected_bits: np.ndarray):
        """Bytes should be convertible to a NumPy bit stego_image."""
        assert np.array_equal(bitops.bytes_to_bits(bytes_to_convert), expected_bits)

    @pytest.mark.parametrize(
        ("bits_to_convert", "expected_bytes"),
        [
            (np.ones(32, dtype=np.uint8), b"\xff\xff\xff\xff"),
            (np.zeros(32, dtype=np.uint8), b"\x00\x00\x00\x00"),
            (np.array([1] + [0] * 31, dtype=np.uint8), b"\x80\x00\x00\x00"),
            (np.ones(8, dtype=np.uint8), b"\xff"),
            (np.empty(0), b""),
        ],
    )
    def test_bits_to_bytes(self, bits_to_convert: np.ndarray, expected_bytes: bytes):
        """NumPy bit stego_image should be convertible to bytes."""
        assert bitops.bits_to_bytes(bits_to_convert) == expected_bytes

    @pytest.mark.parametrize(
        "data",
        [
            b"\xff\xff\xff\xff",
            b"\x00\x00\x00\x00",
            b"\x80\x00\x00\x00",
            b"\xff",
            b"",
        ],
    )
    def test_conversion_equality(self, data: bytes):
        """Bytes should be convertible to bits and back to bytes again."""
        bits = bitops.bytes_to_bits(data)
        assert bitops.bits_to_bytes(bits) == data

    @pytest.mark.parametrize(
        ("byte_array", "bit_index", "expected_bits"),
        [
            (np.array([0xFF, 0xFF, 0xFF], dtype=np.uint8), 0, np.array([1, 1, 1])),
            (np.array([0xFE, 0xFF, 0xFE], dtype=np.uint8), 0, np.array([0, 1, 0])),
            (np.array([0xFC, 0xFC, 0xFE], dtype=np.uint8), 1, np.array([0, 0, 1])),
            (np.array([0x3F, 0xFF], dtype=np.uint8), 7, np.array([0, 1])),
        ],
    )
    def test_get_bit(
        self, byte_array: np.ndarray, bit_index: int, expected_bits: np.ndarray
    ):
        """The nth bits should be extractable from a NumPy byte stego_image."""
        assert np.array_equal(bitops.get_bit(byte_array, bit_index), expected_bits)

    @pytest.mark.parametrize(
        ("byte_array", "bit_array", "bit_index", "expected_bytes"),
        [
            (
                np.array([0xFF, 0xFF, 0xFF], dtype=np.uint8),
                np.array([0, 1, 0], dtype=np.uint8),
                0,
                np.array([0xFE, 0xFF, 0xFE], dtype=np.uint8),
            ),
            (
                np.array([0xFE, 0xFF, 0xFE], dtype=np.uint8),
                np.array([1, 0, 1], dtype=np.uint8),
                0,
                np.array([0xFF, 0xFE, 0xFF], dtype=np.uint8),
            ),
            (
                np.array([0xFF, 0xFF, 0xFF], dtype=np.uint8),
                np.array([0, 0, 1], dtype=np.uint8),
                1,
                np.array([0xFD, 0xFD, 0xFF], dtype=np.uint8),
            ),
            (
                np.array([0x00, 0xFF], dtype=np.uint8),
                np.array([1, 0], dtype=np.uint8),
                7,
                np.array([0x80, 0x7F], dtype=np.uint8),
            ),
        ],
    )
    def test_embed_bits_in_bytes(
        self,
        byte_array: np.ndarray,
        bit_array: np.ndarray,
        bit_index: int,
        expected_bytes: np.ndarray,
    ):
        """Bits should be embedded in the nth position of a NumPy byte stego_image."""
        assert np.array_equal(
            bitops.embed_bits_in_bytes(byte_array, bit_array, bit_index), expected_bytes
        )
