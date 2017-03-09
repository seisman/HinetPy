Data conversion
===============

Hi-net provide waveform data in win32 format and instrument response in channel
table. :mod:`~HinetPy.win32` can convert them into SAC and SACPZ format.

>>> from HinetPy import win32
>>> data = "0101_201001010000_20.cnt"
>>> ctable = "0101_20100101.ch"

Extract Waveform Data
---------------------

Extract all channels from data as SAC format.

>>> win32.extract_sac(data, ctable)

The default filename has a format of "STATION.COMPONENT.SAC" (``N.NABC.U.SAC``).
You can specify another SAC suffix and a different output directory.

>>> win32.extract_sac(data, ctable, suffix="", outdir="SAC")

If you want to extract only a small subset of channels, you can use ``filter_by_id``,
``filter_by_name`` and/or ``filter_by_component`` to filter the channels.
They can accept a list of string or a string contains wildcard.

>>> # extract 3 channles by id
>>> win32.extract_sac(data, ctable, filter_by_id=['3e83', '3e84', '3e85'])
>>> # extract all channels whose name match 'N.NA*'
>>> win32.extract_sac(data, ctable, filter_by_name='N.NA*')
>>> # extract vertical(U) component channels whose name match 'N.NA*'
>>> win32.extract_sac(data, ctable, filter_by_name='N.NA*', filter_by_component='U')

Extract PZ
----------

:meth:`~HinetPy.win32.extract_pz` can convert Hi-net channel table to SAC PZ
format. Its usage is very similar to :meth:`~HinetPy.win32.extract_sac`.

Extract all channels information from channel table:

>>> win32.extract_pz(ctable)

The default filename has a format of "STATION.COMPONENT.SAC_PZ" (``N.NABC.U.SAC_PZ``).
You can specify another SAC suffix and a different output directory.

>>> win32.extract_pz(data, ctable, suffix="SACPZ", outdir="PZ/")

If you want to extract only a small subset of channels, you can use ``filter_by_id``,
``filter_by_name`` and/or ``filter_by_component`` to filter the channels.
They can accept a list of string or a string contains wildcard.

>>> # extract 3 channles by id
>>> win32.extract_pz(ctable, filter_by_id=['3e83', '3e84', '3e85'])
>>> # extract all channels whose name match 'N.NA*'
>>> win32.extract_pz(ctable, filter_by_name='N.NA*')
>>> # extract vertical(U) component channels whose name match 'N.NA*'
>>> win32.extract_pz(ctable, filter_by_name='N.NA*', filter_by_component='U')

.. seealso::

   1. `Response of Observation Equipment <https://hinetwww11.bosai.go.jp/auth/seed/?LANG=en>`_
   2. `Hi-net FAQ Q08 <http://www.hinet.bosai.go.jp/faq/?LANG=en#Q08>`_
