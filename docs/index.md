This project contains Python scripts to request, download and process continuous waveform data
avaiable from [NIED Hi-net][] website.

## Dependency ##

- Python 3.3+
- Python modules: [requests](http://docs.python-requests.org), [clint](https://github.com/kennethreitz/clint), [docopt](http://docopt.org/)
- Hinet [win32tools][]: `catwin32` and `win2sac_32` in your `PATH`

## How to get ##

- Git users: `git clone https://github.com/seisman/HinetScripts.git`

- Other users: [Download ZIP](https://github.com/seisman/HinetScripts/archive/master.zip)

## Before you use it ##

1. Make sure your Python version >= 3.3. If you are new to Python, I strongly
   recommend installing the [Anaconda  Python distribution](https://www.continuum.io/downloads).
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




[win32tools]: https://hinetwww11.bosai.go.jp/auth/manual/dlDialogue.php?r=win32tools
[NIED Hi-net]: http://www.hinet.bosai.go.jp
