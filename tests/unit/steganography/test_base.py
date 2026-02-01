import pytest

from stegos.steganography.base import (
    ImageSteganographyStrategy,
    ImageSteganographyContext,
)
from stegos.steganography.exception import InsufficientCapacityException
from tests.unit.steganography.util import create_image


class DummyStrategy(ImageSteganographyStrategy):
    def payload_capacity(self, cover_image):
        return 10000

    def embed(self, cover_image, payload):
        return cover_image

    def extract(self, stego_image):
        return b""


@pytest.fixture
def steg():
    return ImageSteganographyContext(DummyStrategy())


class TestImageSteganographyContext:
    """Tests for ImageSteganographyContext."""

    def test_embed_empty(self, steg):
        with pytest.raises(ValueError):
            steg.embed(create_image(), b"")

    def test_embed_exceeds_capacity(self, steg):
        steg.strategy.payload_capacity = lambda img: 0
        with pytest.raises(InsufficientCapacityException):
            steg.embed(create_image(), b"x")

    def test_embed_calls_strategy(self, steg):
        cover = create_image()
        assert steg.embed(cover, b"x") is cover
