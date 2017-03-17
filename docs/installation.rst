Installation
============

Python3
-------

HinetPy need Pyhon 3.4 or above. If you're new to Python, I strongly recommend installing the `Anaconda`_.

.. _Anaconda: https://www.continuum.io/downloads

.. note::

   There is no plan to support Python 2.7.

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

::

    tar -xvf win32tools.tar.gz
    cd win32tools/
    make
    cp catwin32.src/catwin32 win2sac.src/win2sac $HOME/bin/

For macOS users, if you fail with an fatal error as below::

    s4read_data.c:3:13: fatal error: 'malloc.h' file not found
    #include    <malloc.h>
                ^
    1 error generated.
    make[1]: *** [s4read_data.o] Error 1

Just edit line 3 of ``win2sac.src/s4read_data.c``, and change ``#include <malloc.h>``
to ``#include <stdlib.h>``.

.. _NIED Hi-net: http://www.hinet.bosai.go.jp/
.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools

HinetPy
-------

To install the latest release version::

    pip install HinetPy

To install the latest developing version::

    git clone https://github.com/seisman/HinetPy
    cd HinetPy
    python setup.py install
