from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'julia_set',
        ['jea/julia_set.cpp'],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True)
        ],
        language='c++'
    ),
]

setup(
    name='JEA',
    version='0.0.1',
    author='Evan Porter',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.5'],
    zip_safe=False,
)
