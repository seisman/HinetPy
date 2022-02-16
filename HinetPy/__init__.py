"""
HinetPy
=======

HinetPy is a Python package to request and process seismic waveform data
from the NIED Hi-net website.

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
# pylint: disable=invalid-name

from pkg_resources import get_distribution

from .client import Client
from .header import NETWORK

__all__ = ["Client", "NETWORK", "win32"]
# Get semantic version through setuptools-scm
__version__ = f'v{get_distribution("HinetPy").version}'  # e.g. v0.1.2.dev3+g0ab3cd78
