from stegos.steganography import bitops

import numpy as np

from stegos.steganography.algorithms.lsb import LSBSteganography


class LossyLSBSteganography(LSBSteganography):
    """Lossy LSB steganography algorithm that embeds in the non-zero coefficients of an image."""

    def _filter_coefs(self, coefs: np.ndarray):
        mask = bitops.has_msb_set(bitops.int32_to_bits(coefs), self.lsb_depth)
        return np.arange(len(coefs))[mask]

    def embed(self, cover_image, payload):
        coefs: np.ndarray = cover_image.ravel()
        mask = self._filter_coefs(coefs)
        coefs[mask] = super().embed(coefs[mask], payload)
        return coefs.reshape(cover_image.shape)

    def extract(self, stego_image):
        coefs: np.ndarray = stego_image.ravel()
        mask = self._filter_coefs(coefs)
        return super().extract(coefs[mask])
