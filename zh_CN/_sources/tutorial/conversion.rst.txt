Data conversion
===============

Hi-net provide waveform data in win32 format and instrument responses in a channel
table. :mod:`~HinetPy.win32` can convert them into SAC and SAC polezero formats.

>>> from HinetPy import win32
>>> data = "0101_201001010000_20.cnt"
>>> ctable = "0101_20100101.ch"

Extract Waveform Data
---------------------

Extract waveform data of all channels as SAC format.

>>> win32.extract_sac(data, ctable)

.. important::

    The SAC files converted from win32 format are **NOT** in digital counts!!!

    ``win2sac_32`` automatically removes sensitivity from waveforms and 
    multipy by 1.0e9. Thus, the SAC files are velocity in nm/s or 
    accelaration in nm/s/s.

The SAC files have a default filename ``STATION.COMPONENT.SAC`` (e.g. ``N.NABC.U.SAC``).
You can specify another SAC suffix and a different output directory.

>>> win32.extract_sac(data, ctable, suffix="", outdir="SAC")

If you want to extract only a small subset of channels, you can use ``filter_by_id``,
``filter_by_name`` and/or ``filter_by_component`` to filter the channels.
They accept a list of string or a string contains wildcard.

>>> # extract 3 channles by id
>>> win32.extract_sac(data, ctable, filter_by_id=['3e83', '3e84', '3e85'])
>>> # extract all channels whose name match 'N.NA*'
>>> win32.extract_sac(data, ctable, filter_by_name='N.NA*')
>>> # extract vertical(U) component channels whose name match 'N.NA*'
>>> win32.extract_sac(data, ctable, filter_by_name='N.NA*', filter_by_component='U')

Extract PZ
----------

:meth:`~HinetPy.win32.extract_pz` can convert instrumental responses 
from Hi-net's channel table to SAC PZ format.

.. warning::

    This function works for Hi-net network only. 

    F-net data users are highly recommended to use `FnetPy <https://github.com/seisman/FnetPy>`_
    to request waveform data in SEED format and extract instrumental responses
    in RESP or PZ format from SEED files.

Extract information of all channels as SACPZ file:

>>> win32.extract_pz(ctable)

The SACPZ file has a default name ``STATION.COMPONENT.SAC_PZ`` (e.g. ``N.NABC.U.SAC_PZ``).
You can specify another SACPZ suffix and a different output directory.

>>> win32.extract_pz(ctable, suffix="SACPZ", outdir="PZ/")

If you want to extract only a small subset of channels, you can use ``filter_by_id``,
``filter_by_name`` and/or ``filter_by_component`` to filter the channels.
They accept a list of string or a string contains wildcard.

>>> # extract 3 channles by id
>>> win32.extract_pz(ctable, filter_by_id=['3e83', '3e84', '3e85'])
>>> # extract all channels whose name match 'N.NA*'
>>> win32.extract_pz(ctable, filter_by_name='N.NA*')
>>> # extract vertical(U) component channels whose name match 'N.NA*'
>>> win32.extract_pz(ctable, filter_by_name='N.NA*', filter_by_component='U')

.. seealso::

   1. `Response of Observation Equipment <https://hinetwww11.bosai.go.jp/auth/seed/?LANG=en>`_
   2. `Hi-net FAQ Q08 <http://www.hinet.bosai.go.jp/faq/?LANG=en#Q08>`_

.. _NIED F-net: http://www.fnet.bosai.go.jp/top.php
