from abc import ABC, abstractmethod


class BaseDH(ABC):
    """Abstract base class defining a Diffie-Hellman Key Exchange algorithm."""

    @abstractmethod
    def exchange(self, peer_public_key: bytes) -> bytes:
        """
        Generates a shared secret key.
        :param peer_public_key: Public key used to generate a shared key between two parties.
        :return: Shared secret key.
        """
        pass

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """
        Gets the public key for exchange.
        :return: Public key used to derive a shared secret.
        """
        pass
