## HinetDoctor.py ##

`HinetDoctor.py` checks whether your configures goes right, you should run it
everytime after you modify `Hinet.cfg`.

Checklist:

1. Python version >= 3.3
2. All third-party modules installed
3. Correct username and password
4. Version of Hi-net website
5. Binary `catwin32` and `win2sac_32` in PATH and executable
6. Number of stations selected for Hi-net and F-net
7. `Maxspan` in allowed range

## StationSelector.py ##

`StationSelector.py` is used to select stations you want to request data.
In most cases, you should use the web version provided by Hi-net website.
This script is only for people who need to change stations frequently.

### Usage ###

```
Select Hi-net/F-net stations to request waveform data from NIED

Usage:
    StationSelector.py -c CODE [-l LIST]
    StationSelector.py -h

Options:
    -h, --help              Show this help.
    -c CODE, --code=CODE    Network code. Hi-net: 0101, F-net: 0103.
    -l LIST, --list=LIST    Station list file.
```

### Notes ###

1. You can only select stations of Hi-net or F-net.
2. All stations will be selected if `-l` options is **NOT** used.
3. List file contains station list, one station per line, lines start with `#` will be ignored.
4. This script does **NOT** check whether a station belongs to a network.
5. You may need to run `HinetDoctor.py` again to check your station selection.

### Examples ###

1. Select all stations of Hi-net

        $ python StationSelector.py -c 0101

2. Select several stations list in a file:

        $ cat sta.list
        N.FJ2H
        N.OTWH
        N.IICH
        N.SMGH
        $ python StationSelector.py -c 0101 -l sta.list


## HinetContRequest.py ##

`HinetContRequest.py` is used to request and download data from NIED server.

### Usage ###

```
$ python HinetContRequest.py -h
Request continuous waveform data from NIED Hi-net.

Usage:
    HinetContRequest.py <year> <month> <day> <hour> <min> <span> [options]
    HinetContRequest.py -h

Arguments for continuous waveform data:
    <year>, <month>, <day>, <hour>, <min>: Starting time in JST time.
    <span>:                                Duration in minutes.

Options:
    -h, --help              Show this help.
    -c CODE --code=CODE     Select code for organization and network.
    -m SPAN --maxspan=SPAN  Max time span for sub-requests
    -d DIR --directory=DIR  Output directory. Default: current directory.
    -o FILE --output=FILE   Output filename.
                            Default: CODE_YYYYMMDDHHMM_SPAN.cnt
    -t FILE --ctable=FILE   Channel table filename. Default: CODE_YYYYMMDD.ch
```

### Examples ###

1.  Request data of Hi-net starting from 2010-10-01T15:00:00 (**JST**)
    with duration of 20 minutes:

        python HinetContRequest.py 2010 10 01 15 00 20

2.  Request data of F-net starting from 2010-10-01T15:00:00 (**JST**)
    with duration of 20 minutes

        python HinetContRequest.py 2010 10 01 15 00 20 -c 0103

3.  Request data of Hi-net, with customized output directory. (**Highly Recommended**)

        python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600

4.  Request data of Hi-net, with customized output directory and filename

        python HinetContRequest.py 2010 10 01 15 00 20 -d aaa -o aaa.cnt -t aaa.ch

If you run `HinetContRequest.py` in the highly recommender way (Example 3),
you will get a directory `201010010600` with two file inside:
`0101_201010011500_20.cnt` and `0101_20101001.ch`.

    |-- 201010010600
        |-- 0101_201010011500_20.cnt
        `-- 0101_20101001.ch

### Notes ###

1. Starting time is in JST, which is UTC+09:00, nine hour ahead of UTC.
2. `<span>` is in minutes.
3. Options `-o` and `-t` allow you customizing output filenames.
   Since the filename format of cnt file and channel tables are
   hard coded in `rdhinet.py` and `ch2pz.py`, you should **NEVER**
   use these two options unless you are able to modify the source code.

## rdhinet.py ##

`rdhinet.py` is used to extract SAC files from WIN32 file.

### Usage ###

```
Extract SAC data files from NIED Hi-net WIN32 files

Usage:
    rdhinet.py DIRNAME [-C <comps>] [-D <outdir>] [-S <suffix>] [-P <procs>]
    rdhinet.py -h

Options:
    -h          Show this help.
    -C <comps>  Components to extract, delimited using commas.
                Avaiable components are U, N, E, X, Y et al.
                Default to extract all components.
    -D <outdir> Output directory for SAC files.
    -S <suffix> Suffix of output SAC files. Default: no suffix.
    -P <procs>  Parallel using multiple processes.
                Set number of CPUs to <procs> if <procs> equals 0. [default: 0]
```

### Examples ###

1.  Extract all channels

        python rdhinet.py 201010010600

2.  Extract NEU components with suffix 'SAC'

        python rdhinet.py 201010010600 -C U,N,E -S SAC

In most cases, what you need is only `-C` option.

If you run `python rdhinet.py 201010010600 -C U`, you will get SAC files
looks like `N.FRNH.U` under directory `201010010600`.

## ch2py.py ##

`ch2pz.py` is used to extract SAC PZ files from Channel Table file.

### Attentions ###

- `ch2pz.py` only works for components whose input unit is `m/s`.
- `ch2pz.py` may only works for Hi-net short period instruments.
- `ch2pz.py` does **NOT** work for F-net.

### Usage ###

```
$ python ch2pz.py -h
Convert NIED Hi-net Channel Table file to SAC PZ files

Usage:
    ch2pz.py DIRNAME [-C <comps>] [-D <outdir>] [-S <suffix>]

Options:
    -C <comps>    Channel Components to convert. Choose from U,N,E,X,Y et. al.
                  Default to convert all components.
    -D <outdir>   Output directory of SAC PZ files. Use the directory of
                  Channel Table file as default.
    -S <suffix>   Suffix for SAC PZ files. [default: SAC_PZ]
```

### Examples ###

1.  Extract all channels

        python ch2pz.py 201010010600

2.  Extract NEU components

        python ch2pz.py 201010010600 -C U,N,E

In most cases, what you need is only `-C` option.

If you run `python ch2pz.py 201010010600 -C U`, you will get SAC PoleZero
files looks like `N.FRNH.U.SAC_PZ` under directory `201010010600`.
