# python setup.py build_ext --inplace
import os
from sys import platform
print("Found platform:", platform)

from setuptools import find_packages, setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy as np

print(find_packages())

setup(
    name='libttp',
    version='0.1.23',
    url='https://github.com/VicidominiLab/libttp',
    license='CC-BY-NC-4.0',
    author='Mattia Donato',
    author_email='mattia.donato@iit.it',
    description='Libraries for reading the data from time-tagging module (BrightEyes-TTM, https://github.com/VicidominiLab/BrightEyes-TTM)',
    ext_modules=cythonize("libttp/ttpCython.pyx", compiler_directives={'language_level' : "3"}, include_path=[np.get_include()]),
    packages=find_packages(),
    include_dir=[np.get_include()],
    cmdclass={'build_ext': build_ext},
)

