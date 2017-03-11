Installation
============

Python3
-------

HinetPy need Pyhon 3.3 or above. If you're new to Python, I strongly recommend installing the `Anaconda`_.

.. _Anaconda: https://www.continuum.io/downloads

Third-party modules
-------------------

HinetPy is dependent on `requests <http://docs.python-requests.org>`_.
Simply run::

    $ pip install requests

to install it.

win32tools
----------

`win32tools`_ is a collection of tools provided by `NIED Hi-net`_ to process
win32 format data. HinetPy needs ``catwin32`` and ``win2sac_32``. Make sure
that ``catwin32`` and ``win2sac_32`` is in your PATH.

.. _NIED Hi-net: http://www.hinet.bosai.go.jp/
.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools

HinetPy
-------

The simplest way to install HinetPy is::

    pip install HinetPy

Or download HinetPy from `here <https://github.com/seisman/HinetPy/releases>`_,
extract it, change dirctory to it and run::

    $ python setup.py install
