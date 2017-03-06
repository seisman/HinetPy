# -*- coding: utf-8 -*-
"""
HinetPy is a Python module aiming to automate and simplify tedious data
request, downloading and format conversion tasks related to `NIED Hi-net`_.

.. _NIED Hi-net: http://www.hinet.bosai.go.jp/

Dependencies
============

#. Python 3.3+
#. `requests <http://docs.python-requests.org/>`_
#. `win32tools`_ provided by `NIED Hi-net`_

.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools

Features
========

#. Automatically request continuous waveform data from Hi-net
#. Convert win32 data into SAC format
#. Extract instrumental response as SAC PZ file

A simple example
================

It's simple to request a continuous waveform data from Hi-net, convert the
data into SAC format and extract instrumental response as SAC PZ file.

>>> from HinetPy import Client, win32
>>> from datetim import datetime
>>>
>>> # You need a Hi-net account to access their data:
>>> client = Client("username", "password")
>>>
>>> # Let's try to request 20 minutes data since 2010-01-01T00:00(GMT+9) from Hi-net
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> data, ctable = client.get_waveform('0101', starttime, 20)
>>> # The request process takes several minutes due to the unfriendly design of Hi-net
>>> ls  # the downloaded data and corresponding channel table
0101_201001010000_20.cnt 0101_20100101.ch
>>>
>>> # Let's convert win32 data into SAC format
>>> win32.extract_sac(data, ctable)
>>> ls *.SAC
N.NGUH.E.SAC  N.NGUH.U.SAC  N.NNMH.N.SAC
N.NGUH.N.SAC  N.NNMH.E.SAC  N.NNMH.U.SAC
>>>
>>> # Let's extract instrument response as PZ file from channel table
>>> win32.extract_pz(ctable)
>>> ls
N.NGUH.E.SAC_PZ  N.NGUH.U.SAC_PZ  N.NNMH.N.SAC_PZ
N.NGUH.N.SAC_PZ  N.NNMH.E.SAC_PZ  N.NNMH.U.SAC_PZ
"""

__title__ = 'HinetPy'
__repo__ = 'https://github.com/seisman/HinetPy'
__version__ = '0.3.0'
__author__ = 'Dongdong Tian'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013-2017 Dongdong Tian'

from HinetPy.client import Client
from HinetPy import win32

__all__ = ["Client", "win32"]
