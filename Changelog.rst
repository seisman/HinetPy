Changelog
=========

0.4.8:
 - ``get_station_list()``: 
   - must specify a network code
   - support S-net and MeSO-net  

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
