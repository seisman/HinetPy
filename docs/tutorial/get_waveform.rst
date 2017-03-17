Get waveform
============

This tutorial shows how to request waveform data from Hi-net in different ways.

>>> from HinetPy import Client
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)  # JST time

.. note::

   All time are in JST time (GMT+0900).

Simple way
----------

Request 20 minutes data since 2010-01-01T00:00 (GMT+0900) from Hi-net network:

>>> data, ctable = client.get_waveform('0101', starttime, 20)
[2017-03-11 17:46:20] INFO: 2010-01-01 00:00 ~20
[2017-03-11 17:46:20] INFO: [1/4] => 2010-01-01 00:00 ~5
[2017-03-11 17:46:41] INFO: [2/4] => 2010-01-01 00:05 ~5
[2017-03-11 17:46:50] INFO: [3/4] => 2010-01-01 00:10 ~5
[2017-03-11 17:47:04] INFO: [4/4] => 2010-01-01 00:15 ~5
>>> ls
0101_201001010000_20.cnt 0101_20100101.ch

Now we get:

1. ``0101_201001010000_20.cnt``: waveform data in win32 format, default name format is ``CODE_YYYYmmddHHMM_LENGTH.cnt``
2. ``0101_20100101.ch``: ctable (aka channel table, similar to instrument response file),
   default name format is ``CODE_YYYYmmdd.ch``.

.. note::

   Hi-net set three limitations for data request:

   1. Record_Length <= 60 min
   2. Number_of_channels * Record_Length <= 12000 min
   3. Only the latest 150 requested data are kept

   For the example above, Hi-net has about 2350 channels, the record length
   should be no more than 5 minutes. Thus the 20-minutes long data request is
   splitted into four 5-minutes short data subrequests.

Custom way
----------

You can set custom filename for both data and ctable, and also the output
directory.

>>> data, ctable = client.get_waveform('0101', starttime, 20,
...                                    data="201001010000.cnt"
...                                    ctable='0101.ch',
...                                    outdir='201001010000')
[2017-03-11 17:46:20] INFO: 2010-01-01 00:00 ~20
[2017-03-11 17:46:20] INFO: [1/4] => 2010-01-01 00:00 ~5
[2017-03-11 17:46:41] INFO: [2/4] => 2010-01-01 00:05 ~5
[2017-03-11 17:46:50] INFO: [3/4] => 2010-01-01 00:10 ~5
[2017-03-11 17:47:04] INFO: [4/4] => 2010-01-01 00:15 ~5
>>> ls 201001010000/
0101.ch 201001010000.cnt

Smart way
---------

As noted above, Hi-net set three limitations for data request. To request
waveform data much longer than limited, HinetPy follow the steps below:

1. split a long data request into several short sub-requests
2. post all sub-requests and download waveform data segments
3. merge all data segments into one complete data

The splitting and merging procedure is transpancy for end users. However,
if you understand the internal procedure, you can have a higher speed by
choosing a proper parameter value.

The number of sub-requests is determined by the total length of the whole
data request, and the maximum allowed length of each subrequest (``max_span``).
``max_span`` has a default value of 5, which is chosen to fit the need of
requesting all channels of Hi-net.

In some case, you may have less channels to request. For example, F-net has
about 450 channels, you can set max_span a higher value of 26 (12000/450=26),
which helps decrease the number of subrequests and reduce the time costs.

The easiest way to choose a proper value for ``max_span`` is to call
:meth:`~HinetPy.client.Client.get_allowed_span`.

>>> client.get_allowed_span('0103')
27
>>> data, ctable = client.get_waveform('0103', starttime, 20, max_span=27)
[2017-03-11 18:07:06] INFO: 2010-01-01 00:00 ~20
[2017-03-11 18:07:06] INFO: [1/1] => 2010-01-01 00:00 ~20

With ``max_span=27``, HinetPy only need one sub-request to get 20-minutes long
waveform data.
