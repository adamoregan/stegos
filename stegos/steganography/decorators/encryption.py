import numpy as np
from cryptography.fernet import Fernet

from stegos.steganography.decorators.decorator import BaseLSBSteganographyDecorator


class EncryptionDecorator(BaseLSBSteganographyDecorator):
    """Encrypts the payload before embedding."""

    def __init__(self, strategy, key: bytes):
        super().__init__(strategy)
        self._fernet = Fernet(key)

    def embed(self, cover_image: np.ndarray, payload: bytes) -> np.ndarray:
        encrypted_payload = self._fernet.encrypt(payload)
        return self.strategy.embed(cover_image, encrypted_payload)

    def extract(self, stego_image: np.ndarray) -> bytes:
        extracted = super().extract(stego_image)
        return self._fernet.decrypt(extracted)
