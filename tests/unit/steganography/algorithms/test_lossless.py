import numpy as np
import pytest

from stegos.steganography.algorithms.lossless import LosslessSteganographyStrategy
from tests.unit.steganography.util import create_image


@pytest.fixture()
def steg():
    return LosslessSteganographyStrategy(seed=1)


class TestLosslessSteganographyStrategy:
    """Tests for LosslessSteganographyStrategy."""

    @pytest.mark.parametrize(
        ("cover_image", "payload"),
        [
            (create_image(8, 8), b"Embedded Payload"),
            (create_image(8, 8, mode="RGB"), b"Embedded Payload"),
            (create_image(8, 8), create_image(2, 2).tobytes()),
            (create_image(8, 8, mode="RGB"), create_image(2, 2).tobytes()),
        ],
    )
    def test_embed_extract(self, steg, cover_image, payload):
        """Embedding and extracting a payload should return the original payload for grayscale and RGB images."""
        stego_image = steg.embed(cover_image, payload)
        assert steg.extract(stego_image) == payload

    @pytest.mark.parametrize("lsb_depth", range(1, 7))
    def test_embed_extract_lsb_depths(self, lsb_depth: int):
        """Embedding and extracting a payload should work for all LSB depths."""
        cover_image = create_image(8, 8)
        steg = LosslessSteganographyStrategy(seed=1, lsb_depth=lsb_depth)
        max_payload_size = steg.payload_capacity(cover_image)
        payload = (
            np.random.default_rng(seed=1)
            .integers(0, 256, size=max_payload_size, dtype=np.uint8)
            .tobytes()
        )
        stego_image = steg.embed(cover_image, payload)
        assert steg.extract(stego_image) == payload

    def test_embed_randomisation(self, steg):
        """Embedding should be seed-independent. The payload should only be recoverable with the correct seed."""
        cover_image, payload = create_image(8, 8), b"x"
        stego_image = steg.embed(cover_image, payload)
        assert (
            LosslessSteganographyStrategy(seed=steg.seed + 1).extract(stego_image)
            != payload
        )
