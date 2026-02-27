from stegos.cryptography.dh.x25519 import X25519


class TestX25519:
    """Tests for X25519."""

    def test_exchange(self):
        """Shared secret key should be established using public keys."""
        party_1, party_2 = X25519(), X25519()
        party_1_key, party_2_key = party_1.public_key, party_2.public_key
        assert party_1.exchange(party_2_key) == party_2.exchange(party_1_key)

    def test_forward_secrecy(self):
        """Shared secret key establishment should provide forward-secrecy."""
        session = X25519()
        assert session.exchange(session.public_key) != session.exchange(
            session.public_key
        )
