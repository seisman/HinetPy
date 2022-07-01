"""
Build and install the project.
"""
from setuptools import find_packages, setup

NAME = "HinetPy"
AUTHOR = "Dongdong Tian"
AUTHOR_EMAIL = "seisman.info@gmail.com"
LICENSE = "MIT License"
URL = "https://github.com/seisman/HinetPy"
DESCRIPTION = (
    "A Python package to request and process seismic waveform data from NIED Hi-net"
)
KEYWORDS = "Seismology, NIED, Hi-net, Waveform"
with open("README.rst", "r", encoding="utf8") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

PACKAGES = find_packages(exclude=["docs", "tests"])
SCRIPTS = []

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Education",
    f"License :: OSI Approved :: {LICENSE}",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Utilities",
]
INSTALL_REQUIRES = ["requests"]
# Configuration for setuptools-scm
SETUP_REQUIRES = ["setuptools_scm"]
USE_SCM_VERSION = {"local_scheme": "node-and-date", "fallback_version": "unknown"}

if __name__ == "__main__":
    setup(
        name=NAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        use_scm_version=USE_SCM_VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        url=URL,
        scripts=SCRIPTS,
        packages=PACKAGES,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
    )
