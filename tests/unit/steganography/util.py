import numpy as np


def create_image(width=8, height=8, mode="RGB"):
    rng = np.random.default_rng(seed=1)
    if mode == "L":
        data = rng.integers(0, 256, size=(height, width), dtype=np.uint8)
    else:
        data = rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)
    return data
