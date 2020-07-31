"""
Creates a `.app` for Mac OS X


Usage:
    python scripts/mac.py py2app
"""

from setuptools import setup
import setuptools

PACKAGES = []
MODULES = ["pygame"]

APP = ['yaps.py']
OPTIONS = {'argv_emulation': False,
           'packages': PACKAGES,
           'includes': MODULES}
DATA_FILES = []
DATA_FILES = ["data", "lib", "local", "README.md"]

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=setuptools.find_packages(),
    include_package_data=True,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
