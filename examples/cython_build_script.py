
##  FILE DESCRIPTION:
##      Setup file for the Cython module
##      NOTES:
##          Build the Cython module with:
##              "python cython_build_script.py build_ext --build-lib=cython_build/"

import shutil
import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import build_ext

# Clean-up
print("Pre-build clean-up started ...")
if os.path.exists('cython_build'):
    shutil.rmtree('cython_build')
if os.path.exists('build'):
    shutil.rmtree('build')
filelist = [f for f in os.listdir(".") if f.endswith(".c")]
for f in filelist:
    os.remove(f)
print("Pre-build clean-up completed.")

source_files = [
    "cython_module.pyx"
]

ext_modules = [
    Extension(  
        "cython_module",
        source_files,
        include_dirs = [],
        libraries = [],
        library_dirs = []
    )
]

setup(
    name = 'Cython module for the Nim lexer',
    cmdclass = {
        'build_ext':    build_ext,
    },
    ext_modules = ext_modules
)