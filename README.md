# HinetPy

A Python module for requesting, downloading and processing continuous seismic
waveform data from [NIED Hi-net](http://www.hinet.bosai.go.jp).

- Author: [Dongdong Tian](https://github.com/seisman) @ USTC
- Project Homepage: https://seisman.github.io/HinetPy
- Latest Release: [![GitHub release](https://img.shields.io/github/release/seisman/HinetPy.svg)](https://github.com/seisman/HinetPy/releases)

## Features

## Installation

```
pip install HinetPy
```

or

```
python setup.py install
```

## Usage

This example just shows the simple workflow to request, download and process waveform data.

**For complete description and usage, please go to the [Project Homepage](https://seisman.github.io/HinetScripts/).**

This example shows how to request continuous waveform data from 2010-10-01T15:00:00(JST) to 2010-10-01T15:20:00(JST).

**Attention: All time are in JST(GMT+09:00) not UTC! **

```python
>>> from datetime import datetime
>>> starttime = datetime(2010, 10, 1, 15, 0)
>>> client = Client(YourUseNameHere, YourPasswordHere)
>>> client.get_waveform('0101', starttime, 20)
```

## Changelog

0.3.0:
 - rewritten as a Python module

0.2.0:
 - some small fixes and improvements

0.1.0:
 - first public release
 - HinetDoctor.py: check dependencies
 - HinetContRequest.py: request continuous data from Hi-net
 - StationSelector.py: select Hi-net/F-net station before requesting data
 - HinetJMARequest.py: request JMA catalogs from Hi-net website
 - rdhinet.py: convert WIN32 format to SAC format
 - ch2pz.py: extract SAC PZ files from Hi-net channel table files

## License

This project is licensed under the terms of the [MIT license](LICENSE).
