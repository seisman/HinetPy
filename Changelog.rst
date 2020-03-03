Changelog
=========

0.6.6 (2020-03-02):
 - win32.extract_pz cannot filter channels by ID and name (#27)

0.6.5 (2019-12-06):
 - Fix PZ files if dampling constant is zero (#24)

0.6.4 (2019-08-23):
 - Capture exception caused by incorrect channel information (#22)

0.6.3 (2019-06-13):
 - Fix ``select_stations()`` (#19)
 - Rename ``string2datetime()`` to ``to_datetime()``

0.6.2 (2019-05-06):
 - Fix download focal mechanism catalog issue (#18).

0.6.1 (2019-02-20):
 - Fix selecting events in a rectangular region.

0.6.0 (2019-02-19):
 - Support request event waveform data (#16).
 - ``get_waveform()`` is renamed to ``get_continuous_waveform()``.

0.5.2 (2019-02-19):
 - Fix selecting stations in a rectangular region (#17).

0.5.1 (2018-12-08):
 - Fix typo from longtitude to longitude.

0.5.0 (2018-11-21):
 - Fix issues of wrong CONSTANT in SAC polezero file (#8).
 - Fix login failure issue with password longer than 12 characters (#13).

0.4.8 (2018-10-04):
 - ``get_station_list()``: must specify a network code; support S-net and MeSO-net.
 - ``select_stations()``: support S-net and MeSO-net

0.4.7 (2018-10-04):
 - Support S-net and MeSO-net (#9 and #10)
 - Fix an issue when channel table contains blank lines

0.4.6 (2018-03-20):
 - Fix ``Too many open files`` (#6)

0.4.5 (2018-03-07):
 - ``get_station_list()``: return a list of stations
 - ``select_stations()``: support selecting stations in a box or circular region

0.4.4 (2017-11-30):
 - Fix a technical issue related to packaging

0.4.3 (2017-11-30):
 - Add Chinese documentation

0.4.2 (2017-06-18):
 - Fix a bug with requests>=2.17

0.4.1 (2017-06-18):
 - remove tempfile after downloading.

0.4.0 (2017-04-01):
 - ``win32.extract_sac()``: skip if data not exists
 - ``win32.extract_sac()``: support multiple processes to speedup, and
   no longer return values
 - ``Client.get_waveform()``: support multi-threads to speedup
 - Change ``Client.help()`` to ``Client.info()``
 - ``Client.get_waveform()`` now can automatically set ``max_span``
 - ``Client.get_*()`` now support startime in different string formats

0.3.3 (2017-03-17):
 - Change ``network`` to ``NETWORK`` in ``header.py``
 - Add wildcard support to ``win32.merge()``
 - Change ``Client.check_module_release()`` to ``Client.check_package_release()``
 - Support output filename with deep directory
 - Always sort cnt files to avoid merge error
 - Set ``pmax`` to 8640000 by default
 - Fix typos

0.3.2 (2017-03-12):
 - Fix another technical issue related to pypi

0.3.1 (2017-03-12):
 - Fix a technical issue related to pypi

0.3.0 (2017-03-12):
 - Rewritten as a Python package

0.2.0 (2016-08-24):
 - Some small fixes and improvements

0.1.0 (2016-08-04):
 - First public release
 - ``HinetDoctor.py``: check dependencies
 - ``HinetContRequest.py``: request continuous data from Hi-net
 - ``StationSelector.py``: select Hi-net/F-net stations before requesting data
 - ``HinetJMARequest.py``: request JMA catalogs from Hi-net website
 - ``rdhinet.py``: convert WIN32 format to SAC format
 - ``ch2pz.py``: extract SAC PZ files from Hi-net channel table files
