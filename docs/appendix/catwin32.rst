catwin32
========

Merger of two or more data sets saved in WIN32 format.

Usage
------

::

    catwin32 File_1 File_2 ... File_n [-oOutFile | -o OutFile] [-s] [-h] > [OutFile]
        File_n        : Input WIN32 file name (accept wildcard).
        -o OutFile    : Output WIN32 file name. Defaults to stdout if -o is ommitted.
        -s            : Sort by date and channel number. This option is time consuming.
        -h            : This usage print.

By default, ``catwin32`` will merge all input win32 files into one output
win32 file, following the order they appear in arguments list. If the input
files in arguments list is not sorted by date and ``-s`` option is not used,
``win2sac_32`` will fail to convert the output win32 format to SAC format,
resulting an error ``The time is not sort.``

Two ways to solve this issue:

1. use ``-s`` option
2. make sure all the win32 files in arguments list are sorted by date

The first way is safer, but it costs too much time. The second way is prefered.
You can use ``sorted(glob.glob("*.cnt"))`` in Python if the win32 files are
named according to time.

Examples
--------

Merge all win32 files matching ``20100101*.cnt`` into one win32 file::

    catwin32 20100101*.cnt -o 0101_201001010000_5.cnt

Merge several win32 files into one win32 file, sorted by date and
channal number::

    catwin32 1.cnt 2.cnt 3.cnt -o total.cnt -s
