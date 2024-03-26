Installation
============

Prerequisites
-------------

To use HinetPy, you need:

- Python >= 3.7
- win32tools provided by NIED Hi-net (see below for install instructions)
- a Hi-net account (register on Hi-net website to get your user name and password)

Install HinetPy
---------------

To install the latest **release/stable** version::

    python -m pip install HinetPy

Or install the **developing/unstable** version::

    git clone https://github.com/seisman/HinetPy
    cd HinetPy
    python setup.py install

If you want to uninstall HinetPy, just run::

    python -m pip uninstall HinetPy

Build win32tools
----------------

`win32tools`_ is a collection of tools provided by `NIED Hi-net`_ to process
win32 format data. HinetPy needs the ``catwin32`` and ``win2sac_32`` commands
to process the win32 data.

Run the following commands to build win32tools::

    tar -xvf win32tools.tar.gz
    cd win32tools/
    make

For macOS users, the above command may fail with an fatal error like this::

    s4read_data.c:3:13: fatal error: 'malloc.h' file not found
    #include    <malloc.h>
                ^
    1 error generated.
    make[1]: *** [s4read_data.o] Error 1

In this case, you should change ``#include <malloc.h>`` to ``#include <stdlib.h>`` at
line 3 of ``win2sac.src/s4read_data.c``.

After successfully building win32tools, you need to make sure that ``catwin32``
and ``win2sac_32`` are in your PATH. You can simply run the following command
to copy the two commands into your HOME's bin directory::

    cp catwin32.src/catwin32 win2sac.src/win2sac_32 $HOME/bin/

.. _NIED Hi-net: https://www.hinet.bosai.go.jp/
.. _win32tools: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools

