First Try
=========

For new users of Hi-net data, I highly recommand you to request and download
waveform data from Hi-net website and try to process the data with win32tools.
Do all the things **manually** at least one time, make sure that you understand
the whole procedures and the unfriendness and limitations of Hi-net website.

Now let's begin our first tour.

Start python
------------

Run ``python`` (or ``ipython`` if you have it), and make sure you're using
Python 3.4 or above::

    $ python
    Python 3.5.3 |Anaconda custom (64-bit)| (default, Feb 22 2017, 21:13:27)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
    Type "help", "copyright", "credits" or "license" for more information.

Create a Client
---------------

HinetPy provide a :class:`~HinetPy.client.Client` class, which provide several
methods to help you get waveform data.

>>> from HinetPy import Client
>>> client = Client("username", "password")  # use your own account.

.. note::

   You need a Hi-net account to have access to Hi-net waveform data.

Do checks
---------

Let our :meth:`~HinetPy.client.Client.doctor` checks if everything goes right:

>>> client.doctor()
[2017-03-11 16:11:47] INFO: You're using the latest release (v0.4.2).
[2017-03-11 16:11:46] INFO: Hi-net web service is NOT updated.
[2017-03-11 16:11:47] INFO: catwin32: /home/user/bin/catwin32.
[2017-03-11 16:11:47] INFO: win2sac_32: /home/user/bin/win2sac_32.

Congratulations! You're using the latest version of HinetPy, and the Hi-net
web service is NOT updated since the release of HinetPy, which means HinetPy
is still working. And you have ``catwin32`` and ``win2sac_32`` in your PATH.
Everything seems OK.

Network Codes
-------------

Hi-net website provide seismic waveform data from several organizations and
networks, e.g. Hi-net, F-net and V-net. Each network has a unique network code.
In order to request waveform data from specified network, you need to know
the network code. See :meth:`~HinetPy.client.Client.info` for details.

>>> client.info()
0101   : NIED Hi-net
0103   : NIED F-net (broadband)
0103A  : NIED F-net (strong motion)
010501 : NIED V-net (Tokachidake)
010502 : NIED V-net (Tarumaesan)
...
0701   : Tokyo Metropolitan Government
0702   : Hot Spring Research Institute of Kanagawa Prefecture
0703   : Aomori Prefectural Government
0705   : Shizuoka Prefectural Government
0801   : ADEP
>>> client.info('0101')  # get more information about NIED Hi-net (0101)
== Information of Network 0101 ==
Name: NIED Hi-net
Homepage: http://www.hinet.bosai.go.jp/
Starttime: 20040401
No. of channels: 2336

Now we know Hi-net starts from 2004-04-01 and has a total number of
2336 channels (about 780 stations).

Stations
--------

If you want, you can have a quick view of stations of Hi-net and F-net
(Only these two networks are supported).
See :meth:`~HinetPy.client.Client.get_station_list` for details.

>>> stations = client.get_station_list()
>>> for station in stations:
...     print(station)
0101 N.WNNH 45.4883 141.885 -159.06
0101 N.SFNH 45.3346 142.1185 -81.6
0101 N.WNWH 45.2531 141.6334 -130.6
0101 N.WNEH 45.2303 141.8806 -174.6
0101 N.SFSH 45.2163 142.2254 -96.6
...

Hi-net/F-net has a lot of stations. If you only need a few of them, you can
select the stations you want. Hi-net website also provide a web interface to
do that, which is prefered for most cases. If you want to dynamically select
stations in your script, you can try
:meth:`~HinetPy.client.Client.select_stations`.

>>> # select only two stations of Hi-net if you know the station names
>>> client.select_stations('0101', ['N.AAKH', 'N.ABNH'])
>>>
>>> # select Hi-net stations in a box region
>>> client.select_stations('0101', minlatitude=36, maxlatitude=50,
...                        minlongitude=140, maxlongitude=150)
>>>
>>> # select Hi-net stations in a circular region
>>> client.select_stations('0101', latitude=36, longitude=139,
...                        minradius=0, maxradius=3)
>>> # select all Hi-net stations
>>> client.select_stations('0101')
