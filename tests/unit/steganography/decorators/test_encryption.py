import pytest
from cryptography.fernet import Fernet, InvalidToken

from stegos.steganography.decorators.encryption import EncryptionDecorator
from tests.unit.steganography.test_base import DummyStrategy
from tests.util import create_image


@pytest.fixture
def steg():
    return EncryptionDecorator(DummyStrategy(), Fernet.generate_key())


class TestEncryptionDecorator:
    """Tests for EncryptionDecorator."""

    def test_embed_extract(self, steg):
        """Payload should be encrypted before embedding and decrypted when extracted."""
        payload = b"Embedded Payload"
        embedded = steg.embed(create_image(), payload)
        assert steg.strategy._payload != payload
        assert steg.extract(embedded) == payload

    def test_key_failure(self, steg):
        """Decryption should be key-dependent."""
        payload = b"Embedded Payload"
        embedded = steg.embed(create_image(), payload)
        steg2 = EncryptionDecorator(steg.strategy, Fernet.generate_key())
        with pytest.raises(InvalidToken):
            steg2.extract(embedded)
