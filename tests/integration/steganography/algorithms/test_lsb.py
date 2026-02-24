from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from stegos.steganography.algorithms.lsb import LSBSteganography
from tests.unit.steganography.util import create_image


def lossless_compression(stego_image: np.ndarray) -> np.ndarray:
    """
    Simulates lossless compression.
    :param stego_image: Stego image to perform lossless compression on.
    :return: Stego image after lossless compression.
    """
    buf = BytesIO()
    Image.fromarray(stego_image).save(buf, format="PNG")
    return np.array(Image.open(buf))


@pytest.fixture()
def steg():
    return LSBSteganography(seed=1)


class TestLSBSteganography:
    """Integration tests for LSBSteganography."""

    @pytest.mark.parametrize(
        "payload",
        [b"Embedded Payload", create_image(2, 2).tobytes()],
    )
    def test_embed_extract_file(self, steg, payload):
        """Embedding should survive lossless compression."""
        cover_image = create_image()
        stego_image = steg.embed(cover_image, payload)
        assert steg.extract(lossless_compression(stego_image)) == payload
