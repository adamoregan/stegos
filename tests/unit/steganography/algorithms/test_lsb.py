import numpy as np
import pytest

from stegos.steganography.algorithms.lsb import LSBSteganography
from stegos.steganography.exception import (
    InsufficientCapacityException,
    InvalidCoverImageException,
)
from tests.unit.steganography.util import create_image


@pytest.fixture()
def steg():
    return LSBSteganography(seed=1)


class TestLSBSteganography:
    """Tests for LSBSteganography."""

    @pytest.mark.parametrize(
        ("cover_image", "payload"),
        [
            (create_image(), b"Embedded Payload"),
            (create_image(mode="RGB"), b"Embedded Payload"),
            (create_image(), create_image(2, 2).tobytes()),
            (create_image(mode="RGB"), create_image(2, 2).tobytes()),
        ],
    )
    def test_embed_extract(self, steg, cover_image, payload):
        """Embedding and extracting a payload should return the original payload for grayscale and RGB images."""
        stego_image = steg.embed(cover_image, payload)
        assert steg.extract(stego_image) == payload

    @pytest.mark.parametrize("lsb_depth", range(1, 7))
    def test_embed_extract_lsb_depths(self, lsb_depth: int):
        """Embedding and extracting a payload should work for all LSB depths."""
        cover_image = create_image()
        steg = LSBSteganography(seed=1, lsb_depth=lsb_depth)
        max_payload_size = steg._payload_capacity(cover_image.ravel())
        payload = (
            np.random.default_rng(seed=1)
            .integers(0, 256, size=max_payload_size, dtype=np.uint8)
            .tobytes()
        )
        stego_image = steg.embed(cover_image, payload)
        assert steg.extract(stego_image) == payload

    def test_embed_randomisation(self, steg):
        """Embedding should be seed-independent. The payload should only be recoverable with the correct seed."""
        cover_image, payload = create_image(), b"Embedded Payload"
        stego_image = steg.embed(cover_image, payload)
        assert LSBSteganography(seed=steg.seed + 1).extract(stego_image) != payload

    def test_embed_empty(self, steg):
        """Embedding an empty payload should raise an exception."""
        with pytest.raises(ValueError):
            steg.embed(create_image(), b"")

    def test_embed_exceeds_capacity(self, steg):
        """Embedding a payload that is too large should raise an exception."""
        steg._payload_capacity = lambda img: 1
        with pytest.raises(InsufficientCapacityException):
            steg.embed(create_image(), b"Em")

    def test_embed_invalid_cover_image(self, steg):
        """Embedding in an image that is too small should raise an exception."""
        with pytest.raises(InvalidCoverImageException):
            steg.embed(create_image(1, 1), b"Em")
