import pytest
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

from stegos.steganography.decorators.encryption import EncryptionDecorator
from tests.unit.steganography.util import create_image, Dummy


def _lightweight_argon2(salt: bytes) -> Argon2id:
    """
    Provides a default key derivation function for testing purposes.
    :param salt: Salt used for key derivation.
    :return: Argon2id key derivation function.
    """
    return Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=1,
        memory_cost=1 * 8,
        ad=None,
        secret=None,
    )


@pytest.fixture
def steg() -> EncryptionDecorator:
    return EncryptionDecorator(Dummy(), b"password", _lightweight_argon2)


class TestEncryptionDecorator:
    """Tests for EncryptionDecorator."""

    def test_embed_extract(self, steg):
        """Payload should be encrypted before embedding and decrypted when extracted."""
        payload = b"Embedded Payload"
        embedded = steg.embed(create_image(), payload)
        assert steg.strategy._payload != payload
        assert steg.extract(embedded) == payload

    def test_embed_extract_uniqueness(self, steg):
        """Embedding with the same password should not result in the same ciphertext."""
        payload = b"Embedded Payload"
        cover_image = create_image()
        steg.embed(cover_image, payload)
        ciphertext1 = steg.strategy._payload
        steg.embed(cover_image, payload)
        ciphertext2 = steg.strategy._payload
        assert ciphertext1 != ciphertext2

    def test_key_failure(self, steg):
        """Decryption should be key-dependent."""
        payload = b"Embedded Payload"
        embedded = steg.embed(create_image(), payload)
        steg2 = EncryptionDecorator(steg.strategy, b"wrong_password")
        with pytest.raises(InvalidToken):
            steg2.extract(embedded)
