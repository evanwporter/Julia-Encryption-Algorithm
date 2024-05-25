import numpy as np
from typing import Callable
from numbers import Complex
import os

from PIL import Image
from PIL import PngImagePlugin

from .julia_set import julia_set

def encrypt(image_path: str, 
            c: Complex,
            min_coordinate: Complex = -.25 - .25j, 
            max_coordinate: Complex = .25 + .25j, 
            iterations_count: int = 256, 
            threshold: float = 2.):
    
    # https://stackoverflow.com/questions/58399070/how-do-i-save-custom-information-to-a-png-image-file-in-python
    # https://gist.github.com/vlantonov/e5de46679379faad1bf24adc7d65c890
    meta = PngImagePlugin.PngInfo()
    meta.add_text("min_coordinate", str(min_coordinate), zip=True)
    meta.add_text("max_coordinate", str(max_coordinate), zip=True)
    meta.add_text("iterations_count", str(iterations_count), zip=True)
    meta.add_text("threshold", str(threshold), zip=True)
    
    img = np.asarray(Image.open(image_path))
    height, width, _ = img.shape
    
    julia = julia_set(
        c = c,
        min_coordinate = min_coordinate, 
        max_coordinate = max_coordinate, 
        iterations_count = iterations_count, 
        threshold = threshold,
        width = width * 3, 
        height = height
    )    
    
    Image.fromarray((
        (
            img.flatten() + (julia % 256)
        ) % 256
    )[np.argsort(julia)].reshape((height, width, 3)).astype(np.uint8)).save(
        "%s_encrypted.png" % os.path.splitext(image_path)[0], 
        "PNG", 
        pnginfo=meta
    )
    
def decrypt(image_path: str, c: Complex): 
    image = Image.open(image_path)
    img_info = image.info

    img = np.asarray(image)
    height, width, _ = img.shape
        
    julia = julia_set(
        c = c, 
        width = width * 3, 
        height = height, 
        min_coordinate = complex(img_info["min_coordinate"]),
        max_coordinate = complex(img_info["max_coordinate"]),
        iterations_count = int(img_info["iterations_count"]),
        threshold = float(img_info["threshold"])
    )

    Image.fromarray((
        (
            img.flatten()[np.argsort(np.argsort(julia))] - 
            (julia % 256)
        ) % 256       
    ).reshape((height, width, 3)).astype(np.uint8)).save(
        "%s_decrypted.png" % os.path.splitext(image_path)[0], 
        "PNG"
    )
    
# Experimental code to make converting PNG metadata easier
# class ImgPNG(Image.Image):
#     def save(self, path, **kwargs):
#         meta = PngImagePlugin.PngInfo()
#         for key, value in self.info.items():
#             meta.add_text(key, str(val), zip=True)
#         super().save(path, "PNG", pnginfo=meta)