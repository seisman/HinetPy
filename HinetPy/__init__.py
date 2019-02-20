# -*- coding: utf-8 -*-
"""
HinetPy
=======

HinetPy is a Python package to request and process seismic waveform data
from NIED Hi-net website.

Basis usage:

>>> from HinetPy import Client, win32
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> data, ctable = client.get_continuous_waveform('0101', starttime, 20)
>>> win32.extract_sac(data, ctable)
>>> win32.extract_pz(ctable)
"""

__title__ = "HinetPy"
__version__ = "0.6.0"
__author__ = "Dongdong Tian"
__license__ = "MIT"

from .client import Client
from .header import NETWORK

__all__ = ["Client", "NETWORK", "win32"]
