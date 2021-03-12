"""
Build and install the project
"""
from setuptools import find_packages, setup

import versioneer

NAME = "HinetPy"
AUTHOR = "Dongdong Tian"
AUTHOR_EMAIL = "seisman.info@gmail.com"
LICENSE = "MIT"
URL = "https://github.com/seisman/HinetPy"
DESCRIPTION = "A NIED Hi-net web service client and win32 tools for seismologists."
KEYWORDS = "Seismology, NIED, Hi-net, Waveform"
with open("README.rst") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

VERSION = versioneer.get_version()
CMDCLASS = versioneer.get_cmdclass()
PACKAGES = find_packages(exclude=["docs", "tests"])
INSTALL_REQUIRES = ["requests"]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Utilities",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
    cmdclass=CMDCLASS,
)
