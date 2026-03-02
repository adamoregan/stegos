import base64
import os
from typing import Callable, TypeAlias

import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

from stegos.steganography.decorators.decorator import BaseLSBSteganographyDecorator


def _default_argon2(salt: bytes) -> Argon2id:
    """
    Provides a default key derivation function.
    :param salt: Salt used for key derivation.
    :return: Argon2id key derivation function.
    """
    # See rfc9106/section-4
    return Argon2id(
        salt=salt,
        length=32,
        iterations=1,
        lanes=4,
        memory_cost=2**21,
        ad=None,
        secret=None,
    )


KDF: TypeAlias = Callable[[bytes], KeyDerivationFunction]


class EncryptionDecorator(BaseLSBSteganographyDecorator):
    """Encrypts the payload before embedding.

    The encryption key is derived from the given password. The salt used for key derivation is embedded in the image.
    """

    SALT_LENGTH = 16

    def __init__(self, strategy, password: bytes, kdf: KDF = None):
        super().__init__(strategy)
        self._password = password
        self._kdf = kdf or _default_argon2

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derives a key for encryption.
        :param salt: Salt used for key derivation.
        :return: Base64 encoded key.
        """
        key = self._kdf(salt).derive(self._password)
        return base64.urlsafe_b64encode(key)

    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        salt = os.urandom(self.SALT_LENGTH)
        key = self._derive_key(salt)
        payload = salt + Fernet(key).encrypt(payload)
        return self.strategy.embed(cover_image, payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        payload = super().extract(stego_image)
        salt, encrypted_payload = (
            payload[: self.SALT_LENGTH],
            payload[self.SALT_LENGTH :],
        )
        return Fernet(self._derive_key(salt)).decrypt(encrypted_payload)
