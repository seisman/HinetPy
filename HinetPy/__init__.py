# -*- coding: utf-8 -*-
"""
HinetPy
=======

HinetPy is a Hi-net client, written in Python, for seismologists, to request
and process seismic waveform data from Hi-net website.

Basis usage:

>>> from HinetPy import Client, win32
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> data, ctable = client.get_waveform('0101', starttime, 20)
>>> win32.extract_sac(data, ctable)
>>> win32.extract_pz(ctable)
"""

__title__ = 'HinetPy'
__version__ = '0.4.5'
__author__ = 'Dongdong Tian'
__license__ = 'MIT'

from .client import Client
from .header import NETWORK

__all__ = ["Client", "NETWORK", "win32"]
