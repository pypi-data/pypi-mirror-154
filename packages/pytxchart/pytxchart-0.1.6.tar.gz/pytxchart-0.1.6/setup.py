import sys                                             

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.1.6"

ext_modules = [
    Pybind11Extension("pytxchart",
        ["src/PyTxChart/main.cpp", "src/PyTxChart/PyTxChart.cpp", "src/PyTxChart/stdafx.cpp"], 
        define_macros = [('VERSION_INFO', __version__)],
	cxx_std=17
        ),
]

setup(
    name="pytxchart",
    version=__version__,
    author="Nikon",
    author_email="nikon.sp@mail.ru",
    url="https://github.com/pybind/python_example",
    description="A test project using pybind11",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)
