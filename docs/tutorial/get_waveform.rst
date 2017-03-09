Get waveform
============

>>> from HinetPy import Client
>>> from datetime import datetime
>>> client = Client("username", "password")
>>> starttime = datetime(2010, 1, 1, 0, 0)

.. note::

   All time are in JST time (GMT+0900).

Request 20 minutes data since 2010-01-01T00:00 (GMT+0900) from Hi-net network:

>>> data, ctable = client.get_waveform('0101', starttime, 20)
[2017-03-11 17:46:20] INFO: 2010-01-01 00:00 ~20
[2017-03-11 17:46:20] INFO: [1/4] => 2010-01-01 00:00 ~5
[2017-03-11 17:46:41] INFO: [2/4] => 2010-01-01 00:05 ~5
[2017-03-11 17:46:50] INFO: [3/4] => 2010-01-01 00:10 ~5
[2017-03-11 17:47:04] INFO: [4/4] => 2010-01-01 00:15 ~5
>>> ls
0101_201001010000_20.cnt 0101_20100101.ch

The default filename is ``CODE_YYYYmmddHHMM_LENGTH.cnt`` for win32 format data,
and ``CODE_YYYYmmdd.ch`` for ctable (ctable, aka channel table, which is
similar to instrument response file).

You can set customized filename for both data and ctable, and also the output
directory.

>>> data, ctable = client.get_waveform('0101', starttime, 20,
...                                    win32_filename="201001010000.cnt"
...                                    channeltable_filename='0101.ch',
...                                    output_directory='201001010000')
[2017-03-11 17:46:20] INFO: 2010-01-01 00:00 ~20
[2017-03-11 17:46:20] INFO: [1/4] => 2010-01-01 00:00 ~5
[2017-03-11 17:46:41] INFO: [2/4] => 2010-01-01 00:05 ~5
[2017-03-11 17:46:50] INFO: [3/4] => 2010-01-01 00:10 ~5
[2017-03-11 17:47:04] INFO: [4/4] => 2010-01-01 00:15 ~5

By default, HinetPy will split the 20-minutes data request into four
5-minutes (5 is the default value of ``max_span``) subrequests,
to satisfy the Hi-net limitations. In some cases, you can choose a larger
``max_span`` to reduce the number of subrequests, thus decrease the waiting
time. For example, if you want to request data from F-net, which has
about 450 channels, you can set max_span=26 (12000/450=26). If you want to request
data of only 50 Hi-net stations, you can set max_span=60 (12000/150=80>60).

The easiest way to determin a proper value of ``max_span`` is to call
:meth:`~HinetPy.client.Client.get_allowed_span`.

>>> client.get_allowed_span('0103')
27
>>> data, ctable = client.get_waveform('0103', starttime, 20, max_span=27)
[2017-03-11 18:07:06] INFO: 2010-01-01 00:00 ~20
[2017-03-11 18:07:06] INFO: [1/1] => 2010-01-01 00:00 ~20
