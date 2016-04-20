# HinetScripts

- Author: [Dongdong Tian](https://github.com/seisman) @ USTC
- Project Homepage: http://seisman.github.io/HinetScripts
- Last Updated: 2016-04-20

This project contains Python scripts for requesting and processing continuous seismic waveform data from [NIED Hi-net][].


### Dependency

- Python 3.3+
- Python modules:
  [requests](http://docs.python-requests.org),
  [clint](https://github.com/kennethreitz/clint),
  [docopt](http://docopt.org/)
- Hinet [win32tools][]: `catwin32` and `win2sac_32` in your `PATH`


### Download

- Git users: `git clone https://github.com/seisman/HinetScripts.git`
- Others users: [Download ZIP](https://github.com/seisman/HinetScripts/archive/master.zip)


### Quick Example

This example just shows the simple workflow to request, download and process waveform data.

**For complete description and usage, please go to the [Project Homepage](http://seisman.github.io/HinetScripts/).**

~~~bash
$ python HinetDoctor.py
$ python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600
$ python rdhinet.py 201010010600
$ python ch2pz.py 201010010600
~~~

This example shows how to request continuous waveform data from 2010:10:01T15:00:00(+0900) to 2010:10:01T15:20:00(+0900).
If everything goes right, you will have one cnt file, one channel table file,
several SAC files and SAC polezero files under directory `201010010600`.

### License

This project is licensed under the terms of the MIT license.

[win32tools]: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools
[NIED Hi-net]: http://www.hinet.bosai.go.jp
