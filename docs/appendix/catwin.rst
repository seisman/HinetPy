catwin
======

Merger of two or more data sets saved in WIN32 format.

Usage
------

::

    catwin32 File_1 File_2 ... File_n -o OutFile [-s] [-h]
        File_n        : Input WIN32 file name
                      : You may use a wild word character.
        OutFile       : Output WIN32 file name
        -s            : Sort by date
        -h            : This usage print

If ``-s`` option is not used, ``catwin32`` will merge all input win32 files,
following the orders they appear in the arguments list. Thus, if the win32 files
are not sorted by date in arguments list, it will result in a wrong win32 file,
which can not be converted to SAC format.

So, the safer way is to always use ``-s`` to tell ``catwin32`` to sort by date
before merging. However, sorting by date is too much time consuming. The best
way is sorting all files in arguments list.

Examples
--------

::

    catwin32 20100101*.cnt -o 0101_201001010000_5.cnt

::

    catwin32 1.cnt 2.cnt 3.cnt -o total.cnt -s
