#include <complex>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

std::vector<int> julia_set(
    std::complex<double> c,
    std::complex<double> min_coordinate,
    std::complex<double> max_coordinate,
    int width, int height,
    double threshold = 2.0,
    int iterations_count = 256)
{
    double mag = std::sqrt(c.real() * c.real() + c.imag() * c.imag());
    c *= (2.0 / mag);

    std::vector<double> re(width), im(height);
    for (int i = 0; i < width; ++i) {
        re[i] = min_coordinate.real() + i * (max_coordinate.real() - min_coordinate.real()) / (width - 1);
    }
    for (int j = 0; j < height; ++j) {
        im[j] = min_coordinate.imag() + j * (max_coordinate.imag() - min_coordinate.imag()) / (height - 1);
    }

    std::vector<int> julia(width * height, 0);
    double thresh2 = threshold * threshold;

    for (int i = 0; i < width; ++i) {
        for (int j = 0; j < height; ++j) {
            double zr = re[i];
            double zi = im[j];
            int ite = 0;

            while ((zr * zr + zi * zi) < thresh2 && ite < iterations_count) {
                double zr_new = zr * zr - zi * zi + c.real();
                zi = 2.0 * zr * zi + c.imag();
                zr = zr_new;
                ite++;
            }
            julia[j * width + i] = ite;
        }
    }

    return julia;
}

PYBIND11_MODULE(julia_set, m) {
    m.def("julia_set", &julia_set, py::arg("c"),
          py::arg("min_coordinate"), py::arg("max_coordinate"),
          py::arg("width"), py::arg("height"),
          py::arg("threshold") = 2.0, py::arg("iterations_count") = 256);
}
