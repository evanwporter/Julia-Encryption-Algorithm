import numpy as np

def decrypt(image, julia): 
    height, width, _ = image.shape
    return (
        (
            image.flatten()[np.argsort(np.argsort(julia))] - 
            (julia % 256).astype(np.uint8)
        ) % 256       
    ).reshape((height, width, 3))