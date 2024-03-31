.. image:: https://github.com/seisman/HinetPy/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/seisman/HinetPy/actions/workflows/tests.yml
.. image:: https://codecov.io/gh/seisman/HinetPy/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/seisman/HinetPy
.. image:: https://img.shields.io/github/release/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/releases
.. image:: https://img.shields.io/pypi/v/HinetPy.svg
    :target: https://pypi.org/project/HinetPy/
.. image:: https://img.shields.io/pypi/pyversions/HinetPy.svg
    :target: https://pypi.org/project/HinetPy/
.. image:: https://img.shields.io/github/license/seisman/HinetPy.svg
    :target: https://github.com/seisman/HinetPy/blob/main/LICENSE
.. image:: https://zenodo.org/badge/23509035.svg
    :target: https://zenodo.org/badge/latestdoi/23509035

.. placeholder-for-doc-index

`NIED Hi-net <https://www.hinet.bosai.go.jp/>`__ |
`Source Code <https://github.com/seisman/HinetPy>`__ |
`Documentation <https://seisman.github.io/HinetPy>`__ |
`中文文档 <https://seisman.github.io/HinetPy/zh_CN/>`__

----

`HinetPy <https://github.com/seisman/HinetPy>`_ is a Python package to request and
process seismic data from `NIED Hi-net <https://www.hinet.bosai.go.jp/>`__.

Features
========

- Request continuous/event waveform data and event catalog from NIED Hi-net
- Support networks like Hi-net, F-net, V-net, S-net and more
- Select Hi-net/F-net stations based on different criteria
- Convert waveform data from win32 format to SAC format
- Extract instrumental response as SAC polezero file
- Multithreads downloading and conversion to speedup

A simple example
================

Here is an example showing how to use HinetPy to request continuous waveform data from
Hi-net, convert the data into SAC format, and extract instrumental responses as SAC
polezero files.

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from HinetPy import Client, win32

    # You need a Hi-net account to access the data
    client = Client("username", "password")

    # Let's try to request 20-minute data of the Hi-net network (with an internal
    # network code of '0101') starting at 2010-01-01T00:00 (JST, GMT+0900)
    data, ctable = client.get_continuous_waveform("0101", "201001010000", 20)

    # The request and download process usually takes a few minutes
    # waiting for data request ...
    # waiting for data download ...

    # Now you can see the data and corresponding channel table in your working directory
    # waveform data (in win32 format) : 0101_201001010000_20.cnt
    # channel table (plaintext file)  : 0101_20100101.ch

    # Let's convert data from win32 format to SAC format
    win32.extract_sac(data, ctable)

    # Let's extract instrument response as PZ files from the channel table file
    win32.extract_sacpz(ctable)

    # Now you can see several SAC and SAC_PZ files in your working directory

    # N.NGUH.E.SAC  N.NGUH.U.SAC  N.NNMH.N.SAC
    # N.NGUH.N.SAC  N.NNMH.E.SAC  N.NNMH.U.SAC
    # ...
    # N.NGUH.E.SAC_PZ  N.NGUH.U.SAC_PZ  N.NNMH.N.SAC_PZ
    # N.NGUH.N.SAC_PZ  N.NNMH.E.SAC_PZ  N.NNMH.U.SAC_PZ
    # ...

Citation
========

If you find this package useful, please consider citing via:

.. image:: https://zenodo.org/badge/23509035.svg
    :target: https://zenodo.org/badge/latestdoi/23509035

License
=======

This project is licensed under the terms of the MIT license.
