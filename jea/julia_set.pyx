import numpy as np
cimport numpy as np
import cython

from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double complex scale_c(double complex c):
    return 2 * c / sqrt(c.real * c.real + c.imag * c.imag)

@cython.boundscheck(False)
@cython.wraparound(False)
def julia_set(double complex c, 
             double complex min_coordinate, 
             double complex max_coordinate,
             int width, 
             int height, 
             double threshold = 2., 
             int iterations_count = 256):
    cdef:
        double[:] im, re
        np.ndarray[np.int32_t, ndim=2] julia
        double zr, zi, thresh2, cr, ci
        int ite, i, j
        
    c = scale_c(c)
        
    re = np.linspace(min_coordinate.real, max_coordinate.real, width)
    im = np.linspace(min_coordinate.imag, max_coordinate.imag, height)

    julia = np.zeros((height, width), dtype = np.int32)
    thresh2 = threshold * threshold
    
    cr = c.real
    ci = c.imag

    for i in range(width):
        for j in range(height):
            zr = re[i] 
            zi = im[j]
            ite = 0
            while (zr * zr + zi * zi) < thresh2 and ite < iterations_count:
                zr, zi = zr*zr - zi*zi + cr, 2*zr*zi + ci
                ite += 1
            julia[j, i] = ite

    return julia.flatten()
