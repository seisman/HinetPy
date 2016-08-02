This quick start example, shows how to request waveform data from
2010-10-01T15:00:00(+0900) to 2010-10-01T15:20:00(+0900):

```
$ python HinetDoctor.py
$ python HinetContRequest.py 2010 10 01 15 00 20 -d 201010010600
$ python rdhinet.py 201010010600
$ python ch2pz.py 201010010600
```

If everything goes right, you will have one cnt file, one channel table file,
several SAC files and SAC polezero files under directory `201010010600`.
