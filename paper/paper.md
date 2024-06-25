---
title: 'HinetPy: A Python package for accessing and processing NIED Hi-net seismic data'
tags:
  - Python
  - geophysics
  - seismology
authors:
 - name: Dongdong Tian
   orcid: 0000-0001-7967-1197
   affiliation: 1
affiliations:
 - name: Hubei Subsurface Multi-scale Imaging Key Laboratory, School of Geophysics and Geomatics, China University of Geosciences, Wuhan 430074, China
   index: 1
date: 3 April 2024
bibliography: paper.bib
---

# Summary

HinetPy is a Python package designed for researchers working with seismic data from the
National Research Institute for Earth Science and Disaster Resilience (NIED) Hi-net
(High-sensitivity seismograph network) in Japan. The seismic network comprises approximately
800 stations with high-quality seismic data. Accessing and processing the data can be
challenging due to the limited functionality of the web UI and backend data server.
Additionally, the seismic data is stored in a non-standard format, which adds an extra
layer of complexity. HinetPy solves these challenges by offering a user-friendly interface
for accessing seismic data from NIED Hi-net and converting it to commonly used data
formats. It streamlines the workflow for seismologists, enabling them to more effectively
utilize this valuable dataset.

# Statement of need

The National Research Institute for Earth Science and Disaster Resilience (NIED) operates
and maintains NIED Hi-net, a nationwide high-sensitivity seismograph network in Japan.
Since its establishment in October 2000, NIED Hi-net has grown to include approximately
800 seismic stations equipped with three-component short-period seismometers [@Obara2005; @Okada2014].
The NIED Hi-net website ([https://www.hinet.bosai.go.jp/](https://www.hinet.bosai.go.jp/))
provides access to high-quality seismic data from 2004 onwards, including data from
other seismic networks such as F-net, S-net, V-net, and more. The NIED Hi-net data has
been widely used in various research from the study of earthquakes [e.g., @Ishii2005; @Peng2007]
to the structure of the Earth's deep interior [e.g., @Niu2005; @Yee2014; @Tian2017].
Despite the value of the data provided by NIED Hi-net, accessing and processing it can be challenging.

## Challenges in accessing NIED Hi-net data

The NIED Hi-net data is available for free through the NIED Hi-net website after users
register for an account. However, accessing them can still be challenging. While most seismic
data centers have transitioned to standard FDSN web services
([https://www.fdsn.org/webservices/](https://www.fdsn.org/webservices/)) in recent years,
allowing users to request seismic data using open-source tools like ObsPy [@ObsPy2015],
NIED Hi-net has not yet upgraded to adopt these services. To request data
from the NIED Hi-net website, users must log in and click many buttons manually.
It is important to note that the NIED Hi-net website has limitations on the data
size and length in a single request. Specifically, the record length of a single channel
cannot exceed 60 minutes, and the total record length of
all channels cannot exceed 12,000 minutes. Considering that NIED Hi-net comprises about 800 seismic
stations and 2,400 channels (3 channels per station), the record length in a single
request must not exceed 5 minutes. If users require 30 minutes of data, they must divide the
time range into six subranges and submit six separate requests. The NIED Hi-net website
does not allow users to post multiple data requests simultaneously. Therefore, to obtain
the requested data, users must post a request, wait for the data to be prepared, and then
post subsequent requests. After all data is ready, users must manually download the files
and combine them into a single file. The entire process can be time-consuming and cumbersome.

## Challenges in processing NIED Hi-net data

NIED Hi-net stores seismic data in a non-standard format called WIN32, accompanied by a
'channels table' text file containing metadata for each channel. Most seismic data processing
software, such as ObsPy, cannot directly use these non-standard formats. Therefore, additional
processing is required to convert the data to commonly used formats, which poses challenges
for researchers. Although NIED Hi-net provides a set of commands in their win32tools package
to process WIN32 data and convert to the SAC format, there are currently no tools available
to convert the channels table to a more commonly used format, such as the SAC polezero file format.
This limitation hinders the broader utilization of NIED Hi-net data.

# HinetPy for easy data accessing and processing

HinetPy is designed to address specific challenges with accessing and processing
NIED Hi-net data through a user-friendly interface. It primarily offers two key components:
the `Client` class for data accessing and the `win32` module for data processing.

The `Client` class utilizes the popular HTTP library [Requests](https://github.com/psf/requests)
to handle user authentication, data requests, status queries, and downloads. This simplifies
the process of accessing NIED Hi-net data, allowing users to access data without any
manual operations on the Hi-net website.

The `win32` module provides several functions for processing WIN32 data, including:

- Merging multiple small WIN32 data files into a single large WIN32 file.
- Converting data from WIN32 format to SAC format.
- Creating instrumental responses in SAC polezero format.

Internally, the `win32` module currently relies on the `catwin32` and `win2sac_32` commands
from the NIED win32tools package for WIN32 data processing. Therefore, the win32tools package
(at least the two required commands) must be installed before using HinetPy.

This is an example demonstrating how to request 20 minutes of waveform data of the Hi-net
network starting at 2010-01-01T00:00 (JST, GMT+0900), convert the data to SAC format
and extract SAC polezero files:
```python
from HinetPy import Client, win32

# You need to register a Hi-net account first
client = Client("username", "password")

# Let's try to request 20-minute data of the Hi-net network (with an internal
# network code of '0101') starting at 2010-01-01T00:00 (JST, GMT+0900)
data, ctable = client.get_continuous_waveform("0101", "201001010000", 20)

# The request and download process usually takes a few minutes.
# Be patient...
# Now you can see the data and channels table in your working directory
# Waveform data (in win32 format) : 0101_201001010000_20.cnt
# Channels table (plaintext file) : 0101_20100101.ch

# Convert data from win32 format to SAC format
win32.extract_sac(data, ctable)
# Extract instrumental responses and save as SAC polezero files
win32.extract_sacpz(ctable)

# Now you can see several SAC and SAC_PZ files in your working directory.
#
# N.NGUH.E.SAC  ...
# N.NGUH.E.SAC_PZ  ...
```

`"0101"` is the internal network code of the Hi-net network. The full list of supported
seismic networks and their internal network codes can be obtained via `client.info()`.

# Key features

The key features of HinetPy are:

1. Facilitates easy access to NIED Hi-net seismic data, including continuous/event waveform
   data and event catalogs.
2. Supports multiple seismic networks (e.g., F-net, S-net, MeSO-net and more in addition
   to Hi-net) in Japan.
3. Selects a subset of stations based on geographical location or station name (Supports
   Hi-net, F-net, S-net and MeSO-net only).
4. Converts waveform data to SAC format and instrumental responses to SAC polezero files.
5. Speeds up the downloading and processing workflow via the use of multithreading.

# Important notes on the use of NIED Hi-net data

1. Users must register an account on the NIED Hi-net website for accessing the data and
   renew the account annually.
2. Users should report their research results using NIED Hi-net data to NIED.
3. Redistribution of any NIED Hi-net data is prohibited.

# Acknowledgments

The HinetPy package was first developed in 2013 by the author during the time as a graduate
student at the University of Science and Technology of China (USTC). It was later maintained
during the author's postdoctoral work at Michigan State University (MSU) and as a faculty
member at the China University of Geosciences, Wuhan. The authors would like to thank
users who report bugs and request features. The author is supported by
the National Natural Science Foundation of China under grant NSFC42274122,
the “CUG Scholar” Scientific Research Funds at China University of Geosciences (Wuhan) (Project No. 2022012),
and the Fundamental Research Funds for the Central Universities, China University of Geosciences (Wuhan) (No. CUG230604).

# References
