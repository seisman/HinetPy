#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from obspy.clients.fdsn import Client as fdsnClient
from obspy import UTCDateTime
from HinetPy import Client, win32


fdsnclient = fdsnClient('IRIS')
starttime = UTCDateTime("2005-01-01")
endtime = UTCDateTime("2005-01-03")
catalog = fdsnclient.get_events(starttime=starttime, endtime=endtime,
                                minmagnitude=6, catalog="ISC")

client = Client("username", "password")
for event in catalog:  # loop over events
    origin = event.origins[0].time.datetime
    starttime = origin + timedelta(hours=9)  # deal with TimeZone issue
    outdir = origin.strftime("%Y%m%d%H%M")

    data, ctable = client.get_waveform('0101', starttime, 20, outdir=outdir)
    win32.extract_sac(data, ctable, outdir=outdir, with_pz=True)
