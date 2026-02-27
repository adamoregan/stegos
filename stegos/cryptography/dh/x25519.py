from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey,
    X25519PrivateKey,
)

from stegos.cryptography.dh.base import BaseDH


class X25519(BaseDH):
    """Elliptic Curve Diffie-Hellman key exchange algorithm.
    Provides forward-secrecy.
    """

    def __init__(self):
        self._private_key = X25519PrivateKey.generate()

    @property
    def public_key(self) -> bytes:
        return self._private_key.public_key().public_bytes_raw()

    def exchange(self, peer_public_key: bytes) -> bytes:
        shared_key = self._private_key.exchange(
            X25519PublicKey.from_public_bytes(peer_public_key)
        )
        self._private_key = X25519PrivateKey.generate()  # provides forward-secrecy
        return shared_key
