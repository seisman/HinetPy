.. image:: https://img.shields.io/travis/seisman/HinetPy/master.svg
    :target: https://travis-ci.org/seisman/HinetPy

.. image:: https://codecov.io/gh/seisman/HinetPy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/seisman/HinetPy

.. image:: https://img.shields.io/github/release/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/releases

.. image:: https://img.shields.io/pypi/v/HinetPy.svg
    :target: https://pypi.org/project/HinetPy/

.. image:: https://img.shields.io/pypi/pyversions/HinetPy.svg
    :target: https://pypi.org/project/HinetPy/

.. image:: https://img.shields.io/github/license/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/blob/master/LICENSE

.. image:: https://zenodo.org/badge/23509035.svg
    :target: https://zenodo.org/badge/latestdoi/23509035

`HinetPy`_ is a Python package to automate and simplify tedious data
request, downloading and format conversion tasks related to `NIED Hi-net`_.

`NIED Hi-net`_ | `Source Code`_ | `Documentation`_ | `中文文档`_

.. _NIED Hi-net: http://www.hinet.bosai.go.jp/
.. _Source Code: https://github.com/seisman/HinetPy
.. _Documentation: https://seisman.github.io/HinetPy
.. _中文文档: https://seisman.github.io/HinetPy/zh_CN/

Feature Support
===============

- Request continuous waveform data from Hi-net
- Select Hi-net/F-net stations inside a box or circular region
- Convert waveform data from win32 format to SAC format
- Extract instrumental response as SAC polezero file
- Multithreads downloading and conversion to speedup

A simple example
================

The power of `HinetPy`_ makes it simple to request continuous waveform data
from Hi-net, convert the data into SAC format and extract instrumental
responses as SAC polezero files.

>>> from HinetPy import Client, win32
>>>
>>> # You need a Hi-net account to access their data
>>> client = Client("username", "password")
>>>
>>> # Let's try to request 20 minutes data since 2010-01-01T00:00(GMT+0900) from Hi-net
>>> # '0101' is the code of Hi-net network
>>> data, ctable = client.get_waveform('0101', '201001010000', 20)
>>> # The request and downloading process usually takes several minutes
>>> # waiting data request ...
>>> # waiting data downloading ...
>>> ls  # the downloaded data and corresponding channel table
0101_201001010000_20.cnt 0101_20100101.ch
>>>
>>> # Let's convert data from win32 format to SAC format
>>> win32.extract_sac(data, ctable)
>>> # Let's extract instrument response as PZ file from channel table
>>> win32.extract_pz(ctable)
>>> ls
N.NGUH.E.SAC  N.NGUH.U.SAC  N.NNMH.N.SAC
N.NGUH.N.SAC  N.NNMH.E.SAC  N.NNMH.U.SAC
...
N.NGUH.E.SAC_PZ  N.NGUH.U.SAC_PZ  N.NNMH.N.SAC_PZ
N.NGUH.N.SAC_PZ  N.NNMH.E.SAC_PZ  N.NNMH.U.SAC_PZ
...

Citation
========

If you find this package useful, please consider citing via:

.. image:: https://zenodo.org/badge/23509035.svg
    :target: https://zenodo.org/badge/latestdoi/23509035

License
=======

This project is licensed under the terms of the `MIT license`_.

.. _HinetPy: https://github.com/seisman/HinetPy
.. _MIT license: license.html
