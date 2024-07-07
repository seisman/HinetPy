# noqa: N999
"""
HinetPy
=======

HinetPy is a Python package for accessing and processing NIED Hi-net seismic data.

Basis usage:

>>> from HinetPy import Client, win32
>>> from datetime import datetime
>>> # You need to provide your Hi-net username and password here!
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> data, ctable = client.get_continuous_waveform("0101", starttime, 20)
>>> win32.extract_sac(data, ctable)
>>> win32.extract_sacpz(ctable)
"""

from importlib.metadata import version

from .client import Client
from .header import NETWORK

__all__ = ["Client", "NETWORK", "win32"]
# Get semantic version through setuptools-scm
__version__ = f'v{version("HinetPy")}'  # e.g. v0.1.2.dev3+g0ab3cd78
