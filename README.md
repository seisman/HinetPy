# Python Scripts for NIED continuous waveform data requesting and processing #

- Author: Dongdong Tian @ USTC
- Update: 2015-07-25

This is a collection of scripts to request, download and process continuous
waveform data avaiable from [NIED Hi-net][] website.

It does not come with any warranties, nor is it guaranteed to work on your
computer. The user assumes full responsibility for the use of all scripts.
The author is **NOT** responsible for any damage that may follow from correct
*or* incorrect use of these scripts.

## Dependency ##

- Python 3.3, 3.4, 3.5 (Python 2 is **NOT** supported)
- Python third-party modules
  - [requests](http://docs.python-requests.org)
  - [clint](https://github.com/kennethreitz/clint)
  - [docopt](http://docopt.org/)
- Hinet [win32tools][]: `catwin32` and `win2sac_32` in your `PATH`

## How to get ##

If you use `git`, just clone it to your working directory:

    git clone https://github.com/seisman/HinetScripts.git

After `git clone`, you can get the latest version anytime with just one command:

    git pull

If you do not use `git`, just click the "Download ZIP" button on the right.

## Before you use it ##

1. Make sure your Python version >= 3.3
2. Install Python third-party modules by `pip install -r requirements.txt`
3. Register on the [NIED Hi-net][] website, so that you have access to NIED
   waveform data
4. Download [win32tools][] and compile it, make sure binary `catwin32` and
   `win2sac_32` are in you PATH
5. Request, download and process data **manually** at least one time, make sure
   that you know the whole procedures and limitations of NIED website
6. Modify `User` and `Password` in configure file `Hinet.cfg`
7. Run `HinetDoctor.py` to check your configure file

If you can read Chinese, [posts](http://seisman.info/hinet-things.html) listed
in my blog may help you understand details.

如果你能读懂中文，我博客列出的一些 [博文](http://seisman.info/hinet-things.html)
会帮助你更好地理解其中的细节。部分博文未及时更新，若有冲突，请以本文为准。

## Quick Start ##

If you want a quick start, just copy and run commands below.

This quick start exmaple, shows how to request waveform data from
2010:10:01T15:00:00(+0900) to 2010:10:01T15:20:00(+0900):

    $ python HinetDoctor.py
    $ python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600
    $ python rdhinet.py 201010010600
    $ python ch2pz.py 201010010600

If everything goes right, you will have one cnt file, one channel table file,
several SAC files and SAC polezero files under directory `201010010600`.

## Scripts ##

### HinetDoctor.py ###

`HinetDoctor.py` checks whether your configures goes right, you should run it
everytime after you modify `Hinet.cfg`.

1. Python version >= 3.3
2. All third-party modules installed
3. Correct username and password
4. Version of Hi-net website
5. Binary `catwin32` and `win2sac_32` in PATH and executable
6. Number of stations selected for Hi-net and F-net?
7. `Maxspan` in allowed range

### StationSelector.py ###

`StationSelector.py` is used to select stations you want to request data.
In most cases, you should use the web version provided by Hi-net website.
This script is only for people who need to change stations frequently.

#### Usage ####

    Select Hi-net/F-net stations to request waveform data from NIED

    Usage:
        StationSelector.py -c CODE [-l LIST]
        StationSelector.py -h

    Options:
        -h, --help              Show this help.
        -c CODE, --code=CODE    Network code. Hi-net: 0101, F-net: 0103.
        -l LIST, --list=LIST    Station list file.

#### Notes ####

1. You can only select stations of Hi-net or F-net.
2. All stations will be selected if -l options is NOT used.
3. List file contains station list, one station per line, lines start with '#'
   will be ignored.
4. This script does **NOT** check whether a station belongs to a network.
5. You may need to run `HinetDoctor.py` again to check your station selection.

#### Examples ####

1. Select all stations of Hi-net

        $ python StationSelector.py -c 0101

2. Select several stations list in a file:

        $ cat sta.list
        N.FJ2H
        N.OTWH
        N.IICH
        N.SMGH
        $ python StationSelector.py -c 0101 -l sta.list

### HinetContRequest.py ###

`HinetContRequest.py` is used to request and download data from NIED server.

#### Usage ####

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

#### Examples ####

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

#### Notes ####

1. Starting time is in JST, which is UTC+09:00, nine hour ahead of UTC.
2. `<span>` is in minutes.
3. Options `-o` and `-t` allow you customizing output filenames.
   Since the filename format of cnt file and channel tables are
   hard coded in `rdhinet.py` and `ch2pz.py`, you should **NEVER**
   use these two options unless you are able to modify the source code.

### rdhinet.py ###

`rdhinet.py` is used to extract SAC files from WIN32 file.

#### Usage ####

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

#### Examples ####

1.  Extract all channels

        python rdhinet.py 201010010600

2.  Extract NEU components with suffix 'SAC'

        python rdhinet.py 201010010600 -C U,N,E -S SAC

In most cases, what you need is only `-C` option.

If you run `python rdhinet.py 201010010600 -C U`, you will get SAC files
looks like `N.FRNH.U` under directory `201010010600`.

### ch2py.py ###

`ch2pz.py` is used to extract SAC PZ files from Channel Table file.

#### Attentions ####

- `ch2pz.py` only works for components whose input unit is `m/s`.
- `ch2pz.py` may only works for Hi-net short period instruments.
- `ch2pz.py` does **NOT** work for F-net.

#### Usage ####

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

#### Examples ####

1.  Extract all channels

        python ch2pz.py 201010010600

2.  Extract NEU components

        python ch2pz.py 201010010600 -C U,N,E

In most cases, what you need is only `-C` option.

If you run `python ch2pz.py 201010010600 -C U`, you will get SAC PoleZero
files looks like `N.FRNH.U.SAC_PZ` under directory `201010010600`.

## FAQ ##

### What is network code? ###

Each network is represented by a network code. For example, Hi-net
network has a code of '0101', while V-net '0105'. You can see the full
code list by running `python HinetContRequest.py -h`.

### What is Maxspan? And how to choose it? ###

NIED Hi-net website sets a limitation of data size in one request:

1. Record Length <= 60 min
2. Number of channels * Record Length <= 12000 min

Just take Hi-net as example, Hi-net network has about 800 station and
24000 channels. According to the limitations, the record length should
be no more than 5 minutes long in one web request. So the `Maxspan`,
allowed maximum record length, should be no more than 5 for Hi-net
network with all stations selected.

The request script `HinetContRequest.py` helps you break through the
limitation. Using this script, you can requst datas with a much longer
record length, this script will split the request into multiple
sub-requests, each has a record length no more than `Maxspan` minutes.

### What's the workflow of HinetContRequest.py ###

1. read configure file
2. login Hi-net website
3. check whether starting time is in service period
4. if `<span>` is larger than `MaxSpan`, split this request into multiple
   sub-requests, each has a duration no larger than `MaxSpan`
5. start the first sub-request, wait until the data is ready, then
   remember the ID
6. repeat step 5 for all sub-requests, and remember all IDs
7. download all datas in zip format
8. unzip all zip files, merge all cnt files into one cnt file
9. rename and cleanup

### What's MaxSleepCount and SleepTime? ###

After posting a data request, Hi-net server will deal with this request and
prepare waveform data. During the preparation, user is not allowed to post
another new request. So user has to wait until the data is ready.

The script will check the status of data preparation. If the data is not ready,
it will sleep for `SleepTime` seconds, and then check the status again, until
the data is ready or the number of checks larger than `MaxSleepCount`.

So the maximum sleep time for one request is MaxSleepCount\*SleepTime seconds,
if the data is still not ready, the script will report a error.

[win32tools]: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools
[NIED Hi-net]: http://www.hinet.bosai.go.jp
