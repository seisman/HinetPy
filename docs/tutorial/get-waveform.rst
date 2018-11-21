Get waveform
============

This tutorial shows how to use :meth:`~HinetPy.client.Client.get_waveform`
to request waveform data from Hi-net in different ways.

.. note::

   All times in HinetPy and Hi-net website are in JST time (GMT+0900).

Basic Usage
-----------

Request 20 minutes data since 2010-01-01T00:00 (GMT+0900) from Hi-net network:

>>> from HinetPy import Client
>>> client = Client("username", "password")
>>> data, ctable = client.get_waveform('0101', '201001010000', 20)
[2017-03-11 17:46:20] INFO: 2010-01-01 00:00 ~20
[2017-03-11 17:46:20] INFO: [1/4] => 2010-01-01 00:00 ~5
[2017-03-11 17:46:41] INFO: [2/4] => 2010-01-01 00:05 ~5
[2017-03-11 17:46:50] INFO: [3/4] => 2010-01-01 00:10 ~5
[2017-03-11 17:47:04] INFO: [4/4] => 2010-01-01 00:15 ~5
>>> ls
0101_201001010000_20.cnt 0101_20100101.ch

:meth:`~HinetPy.client.Client.get_waveform` also supports ``starttime``
in other common used formats:

>>> data, ctable = client.get_waveform('0101', '2010-01-01T00:00', 20)
>>> data, ctable = client.get_waveform('0101', '2010-01-01 00:00', 20)

and :py:class:`datetime.datetime` to allow users manipulate datetimes in a
more flexible way.

>>> from datetime import datetime
>>> starttime = datetime(2010, 1, 1, 0, 0)  # JST time
>>> data, ctable = client.get_waveform('0101', starttime, 20)

Now we get:

1. ``0101_201001010000_20.cnt``: waveform data in win32 format, default name format is ``CODE_YYYYmmddHHMM_LENGTH.cnt``
2. ``0101_20100101.ch``: ctable (aka channel table, similar to instrument response file),
   default name format is ``CODE_YYYYmmdd.ch``.

.. note::

   Hi-net sets three limitations for data request:

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

>>> from HinetPy import Client
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)  # JST time
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
