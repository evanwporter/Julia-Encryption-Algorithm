import numpy as np
from typing import Callable
from numbers import Complex
from functools import partial
from dataclasses import dataclass

def encrypt(img, julia):
    height, width, _ = img.shape
    return (
        (
            img.flatten() + (julia % 256).astype(np.uint8)
        ) % 256
    )[np.argsort(julia)].reshape((height, width, 3))

def decrypt(image, julia): 
    height, width, _ = image.shape
    return (
        (
            image.flatten()[np.argsort(np.argsort(julia))] - 
            (julia % 256).astype(np.uint8)
        ) % 256       
    ).reshape((height, width, 3))

def Q(z: Complex, c: Complex) -> Complex:
    return z ** (2) + c

@dataclass
class julia:
    min_coordinate: Complex = -.25 - .25j
    max_coordinate: Complex = .25 + .25j
    iterations_count: int = 256
    threshold: float = 2.
        
    def bound_num(self, c):
        magnitude = abs(c)
        if magnitude > self.threshold:
            c = c * self.threshold / magnitude
        
        return c
    
        
    def julia_set(self,
                  mapping: Callable[[Complex], Complex],
                  c: Complex,
                  height: int,
                  width: int) -> np.ndarray:
        
        c = self.bound_num(c)
        
        im, re = np.ogrid[self.min_coordinate.imag: self.max_coordinate.imag: height * 1j,
                          self.min_coordinate.real: self.max_coordinate.real: width * 1j]
        z = (re + 1j * im).flatten()

        live, = np.indices(z.shape)  # indexes of pixels that have not escaped
        iterations = np.empty_like(z, dtype=int)

        for i in range(self.iterations_count):
            z_live = z[live] = mapping(z[live], c)
            escaped = abs(z_live) > self.threshold
            iterations[live[escaped]] = i
            live = live[~escaped]
            if live.size == 0:
                break
        else:
            iterations[live] = self.iterations_count

        return iterations#.reshape((height, width))
