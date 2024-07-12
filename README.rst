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
.. image:: https://joss.theoj.org/papers/10.21105/joss.06840/status.svg
   :target: https://doi.org/10.21105/joss.06840
.. image:: https://zenodo.org/badge/23509035.svg
    :target: https://zenodo.org/badge/latestdoi/23509035


`NIED Hi-net <https://www.hinet.bosai.go.jp/>`__ |
`Source Code <https://github.com/seisman/HinetPy>`__ |
`Documentation <https://seisman.github.io/HinetPy>`__ |
`中文文档 <https://seisman.github.io/HinetPy/zh_CN/>`__

----

.. placeholder-for-doc-index

`HinetPy <https://github.com/seisman/HinetPy>`_ is a Python package for accessing and
processing seismic data from `NIED Hi-net <https://www.hinet.bosai.go.jp/>`__.

Key Features
============

- Facilitates easy access to NIED Hi-net seismic data, including continuous/event
  waveform data and event catalogs.
- Supports multiple seismic networks (e.g., F-net, S-net, MeSO-net and more in addition
  to Hi-net) in Japan.
- Selects a subset of stations based on geographical location or station name (Supports
  Hi-net, F-net, S-net and MeSO-net only).
- Converts waveform data to SAC format and instrumental responses to SAC polezero files.
- Speeds up the downloading and processing workflow via the use of multithreading.

A simple example
================

Here is an example showing how to use HinetPy to request continuous waveform data from
Hi-net, convert the data into SAC format, and extract instrumental responses as SAC
polezero files.

.. code-block:: python

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

If you find this package useful, please consider citing the package in either of the
following ways:

**Cite the HinetPy paper (preferred)**

A formal paper is published on `The Journal of Open Source Software <https://joss.theoj.org/>`__
since HinetPy v0.9.0. This is the **preferred** way for citation.

    Tian, D. (2024). HinetPy: A Python package for accessing and processing NIED Hi-net seismic data.
    Journal of Open Source Software, 9(98), 6840. https://doi.org/10.21105/joss.06840

**Cite a specific HinetPy version**

If you'd like to cite a specific HinetPy version, you can visit
`Zenodo <https://zenodo.org/records/12523911>`__, choose the version you want to cite,
and cite like this:

    Tian, D. (20XX). HinetPy: A Python package for accessing and processing NIED Hi-net seismic data (X.X.X).
    Zenodo. https://doi.org/10.5281/zenodo.xxxxxxxx

Contributing
============

Feedback and contributions are welcome! Please feel free to open an issue or pull
request if you have any suggestions or would like to contribute a feature.
For additional information or specific questions, please open an issue directly.

License
=======

This project is licensed under the terms of the MIT license.
