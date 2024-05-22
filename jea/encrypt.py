import numpy as np

def encrypt(img, julia):
    height, width, _ = img.shape
    return (
        (
            img.flatten() + (julia % 256).astype(np.uint8)
        ) % 256
    )[np.argsort(julia)].reshape((height, width, 3))