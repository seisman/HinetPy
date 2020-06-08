#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from codecs import open
from setuptools import setup, find_packages
import versioneer

here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="HinetPy",
    version=versioneer.get_version(),
    description="A NIED Hi-net web service client "
    "and win32 tools for seismologists.",
    long_description=long_description,
    url="https://github.com/seisman/HinetPy",
    author="Dongdong Tian",
    author_email="seisman.info@gmail.com",
    keywords="Seismology, NIED, Hi-net, Waveform",
    license="MIT",
    packages=find_packages(exclude=["docs"]),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Utilities",
    ],
)
