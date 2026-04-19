import numpy as np

from stegos.core.steganography import bitops
from stegos.core.steganography.algorithms.lsb import LSBSteganography


class LossyLSBSteganography(LSBSteganography):
    """Lossy LSB steganography algorithm that embeds in the non-zero coefficients of an image."""

    def embed(self, cover_image, payload):
        coefs: np.ndarray = cover_image.ravel()
        mask = bitops.has_msbs_set(coefs, self.lsb_depth)
        masked = coefs[mask]  # copy, must be written back
        super().embed(masked, payload)
        coefs[mask] = masked

    def extract(self, stego_image):
        coefs: np.ndarray = stego_image.ravel()
        mask = bitops.has_msbs_set(coefs, self.lsb_depth)
        return super().extract(coefs[mask])
