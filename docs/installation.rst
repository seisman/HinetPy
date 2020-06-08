Installation
============

HinetPy needs Pyhon 3.6 or above. If you're new to Python, I strongly recommend
installing the `Anaconda`_ Python distribution.

.. _Anaconda: https://www.anaconda.com/download/

Install HinetPy
---------------

To install the latest **release/stable** version from PyPI::

    pip install HinetPy

To install the **developing/unstable** version::

    pip install git+https://github.com/seisman/HinetPy.git

or::

    git clone https://github.com/seisman/HinetPy
    cd HinetPy
    python setup.py install

If you want to uninstall HinetPy, just run::

    pip uninstall HinetPy

win32tools
----------

`win32tools`_ is a collection of tools provided by `NIED Hi-net`_ to process
win32 format data. HinetPy needs the ``catwin32`` and ``win2sac_32`` commands
to process the win32 data.
Make sure that ``catwin32`` and ``win2sac_32`` are in your PATH.

To install win32tools::

    tar -xvf win32tools.tar.gz
    cd win32tools/
    make
    cp catwin32.src/catwin32 win2sac.src/win2sac_32 $HOME/bin/

For macOS users, if you fail with an fatal error as below::

    s4read_data.c:3:13: fatal error: 'malloc.h' file not found
    #include    <malloc.h>
                ^
    1 error generated.
    make[1]: *** [s4read_data.o] Error 1

You need change ``#include <malloc.h>`` to ``#include <stdlib.h>`` at
line 3 of ``win2sac.src/s4read_data.c``.

.. _NIED Hi-net: http://www.hinet.bosai.go.jp/
.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools

