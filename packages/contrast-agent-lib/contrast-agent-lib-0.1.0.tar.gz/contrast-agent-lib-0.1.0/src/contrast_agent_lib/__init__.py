import ctypes

from sys import platform
from os import path

lib_name = "libcontrast_c"
lib_ext = ".dylib" if platform.startswith("darwin") else ".so"
lib_path = "".join([path.dirname(__file__), "/libs/", lib_name, lib_ext])

lib_contrast = ctypes.cdll.LoadLibrary(lib_path)
