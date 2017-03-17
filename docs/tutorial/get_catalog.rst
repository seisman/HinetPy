Get Catalog
============

Get arrival time catalog
------------------------

Hi-net provide JMA arrivaltime data for downloading.

>>> from HinetPy import Client
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> client.get_arrivaltime(startdate, 5)
'measure_20100101_5.txt'

Get focal mechanism catalog
---------------------------

Hi-net provide JMA focal mechanism catalog for downloading.

>>> from HinetPy import Client
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)
>>> client.get_focalmechanism(startdate, 5)
'focal_20100101_5.txt'
