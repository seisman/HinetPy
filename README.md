# HinetScripts

- Author: [Dongdong Tian](https://github.com/seisman) @ USTC
- Project Homepage: http://seisman.github.io/HinetScripts
- Last Updated: 2015-07-25

This project contains Python scripts for requesting and processing continuous seismic waveform data from [NIED Hi-net][].

It does not come with any warranties, nor is it guaranteed to work on your
computer. The user assumes full responsibility for the use of all scripts.
The author is **NOT** responsible for any damage that may follow from correct
*or* incorrect use of these scripts.


## Dependency

- Python 3.3+
- Python third-party modules
  - [requests](http://docs.python-requests.org)
  - [clint](https://github.com/kennethreitz/clint)
  - [docopt](http://docopt.org/)
- Hinet [win32tools][]: `catwin32` and `win2sac_32` in your `PATH`


## Download

- Git users: `git clone https://github.com/seisman/HinetScripts.git`
- Others users: [Download ZIP](https://github.com/seisman/HinetScripts/archive/master.zip)


## Quick Example

This example just shows the simple workflow to request, download and process waveform data.

**For complete description and usage, please go to the [Project Homepage](http://seisman.github.io/HinetScripts/).**

```
$ python HinetDoctor.py
$ python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600
$ python rdhinet.py 201010010600
$ python ch2pz.py 201010010600
```

This example shows how to request continuous waveform data from 2010:10:01T15:00:00(+0900) to 2010:10:01T15:20:00(+0900).
If everything goes right, you will have one cnt file, one channel table file,
several SAC files and SAC polezero files under directory `201010010600`.


[win32tools]: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools
[NIED Hi-net]: http://www.hinet.bosai.go.jp
