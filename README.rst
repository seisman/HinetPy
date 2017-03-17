.. image:: https://img.shields.io/travis/seisman/HinetPy/master.svg
    :target: https://travis-ci.org/seisman/HinetPy

.. image:: https://img.shields.io/github/release/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/releases

.. image:: https://img.shields.io/pypi/v/HinetPy.svg
    :target: https://pypi.python.org/pypi/HinetPy/

.. image:: https://img.shields.io/github/license/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/HinetPy.svg
    :target: https://pypi.python.org/pypi/HinetPy/

`HinetPy`_ is a Python package aiming to automate and simplify tedious data
request, downloading and format conversion tasks related to `NIED Hi-net`_.

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
>>> from datetime import datetime
>>>
>>> # You need a Hi-net account to access their data
>>> client = Client("username", "password")
>>>
>>> # Let's try to request 20 minutes data since 2010-01-01T00:00(GMT+0900) from Hi-net
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> data, ctable = client.get_waveform('0101', starttime, 20)
>>> # The request process takes several minutes due to the unfriendly design of Hi-net
>>> ls  # the downloaded data and corresponding channel table
0101_201001010000_20.cnt 0101_20100101.ch
>>>
>>> # Let's convert win32 data into SAC format
>>> sacfiles = win32.extract_sac(data, ctable)
>>> ls *.SAC
N.NGUH.E.SAC  N.NGUH.U.SAC  N.NNMH.N.SAC
N.NGUH.N.SAC  N.NNMH.E.SAC  N.NNMH.U.SAC
...
>>>
>>> # Let's extract instrument response as PZ file from channel table
>>> pzfiles = win32.extract_pz(ctable)
>>> ls *.SAC_PZ
N.NGUH.E.SAC_PZ  N.NGUH.U.SAC_PZ  N.NNMH.N.SAC_PZ
N.NGUH.N.SAC_PZ  N.NNMH.E.SAC_PZ  N.NNMH.U.SAC_PZ
...

License
=======

This project is licensed under the terms of the MIT license.

.. _HinetPy: https://seisman.github.io/HinetPy
.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools
.. _NIED Hi-net: http://www.hinet.bosai.go.jp/
