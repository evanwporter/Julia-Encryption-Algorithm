import numpy as np
from typing import Callable
from numbers import Complex
import os

from PIL import Image
from PIL import PngImagePlugin

from .julia_set import julia_set

# def _Q(z: Complex, c: Complex) -> Complex:
#     return z ** (2) + c
        
def _scale_c(c):
    # f : c -> c'
    # function is injective (one to one)
    return 2*c / abs(c)
        
# def _julia_set(mapping: Callable,
#               c: Complex,
#               height: int,
#               width: int,
#               min_coordinate: Complex,
#               max_coordinate: Complex,
#               iterations_count: int,
#               threshold: float) -> np.ndarray:
    
#     # https://rosettacode.org/wiki/Julia_set#Vectorized
#     # https://codereview.stackexchange.com/a/224349

#     c = _scale_c(c)

#     im, re = np.ogrid[min_coordinate.imag: max_coordinate.imag: height * 1j,
#                       min_coordinate.real: max_coordinate.real: width * 1j]
#     z = (re + 1j * im).flatten()

#     live, = np.indices(z.shape)  # indexes of pixels that have not escaped
#     iterations = np.empty_like(z, dtype=int)

#     for i in range(iterations_count):
#         z_live = z[live] = mapping(z[live], c)
#         escaped = z_live.real ** 2 + z_live.imag ** 2 > threshold ** 2 # see ref (2) above
#         iterations[live[escaped]] = i
#         live = live[~escaped]
#         if live.size == 0:
#             break
#     else:
#         iterations[live] = iterations_count

#     return iterations

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