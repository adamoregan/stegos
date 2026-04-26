from PySide6.QtCore import QObject, Signal

from stegos.core.cryptography.dh.base import BaseDH


class DHModel(QObject):
    """Model for Diffie-Hellman Key Exchange.

    Emits key change and error signals.
    """

    publicKeyChanged = Signal(bytes)
    sharedKeyGenerated = Signal(bytes)
    error = Signal()

    def __init__(self, dh: BaseDH):
        """
        Creates an instance of the DHModel class.
        :param dh: Diffie-Hellman Key Exchange algorithm.
        """
        super().__init__()
        self._dh = dh

    def exchange(self, peer_public_key: bytes) -> None:
        """
        Generates a shared secret key.
        :param peer_public_key: Public key used to generate a shared key between two parties.
        """
        try:
            shared_key = self._dh.exchange(peer_public_key)
            self.sharedKeyGenerated.emit(shared_key)
            self.publicKeyChanged.emit(self._dh.public_key)
        except ValueError:
            self.error.emit()

    @property
    def public_key(self) -> bytes:
        """
        Gets the public key for exchange.
        :return: Public key used to derive a shared secret.
        """
        return self._dh.public_key

    def rotate(self) -> None:
        """Rotates the public key."""
        self._dh.rotate()
        self.publicKeyChanged.emit(self._dh.public_key)
