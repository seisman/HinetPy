# HinetScripts

- Author: [Dongdong Tian](https://github.com/seisman) @ USTC
- Project Homepage: https://seisman.github.io/HinetScripts

This project contains Python scripts for requesting and processing continuous seismic waveform data from [NIED Hi-net][].


## Quick Preview

This example just shows the simple workflow to request, download and process waveform data.

**For complete description and usage, please go to the [Project Homepage](https://seisman.github.io/HinetScripts/).**

~~~bash
$ python HinetDoctor.py
$ python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600
$ python rdhinet.py 201010010600
$ python ch2pz.py 201010010600
~~~

This example shows how to request continuous waveform data from 2010-10-01T15:00:00(JST) to 2010-10-01T15:20:00(JST).
If everything goes right, you will have one cnt file, one channel table file,
several SAC files and SAC polezero files under directory `201010010600`.

## License

This project is licensed under the terms of the MIT license.

[NIED Hi-net]: http://www.hinet.bosai.go.jp
