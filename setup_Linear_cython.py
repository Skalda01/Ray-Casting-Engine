from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("Cython/Linear_cython.pyx")
)