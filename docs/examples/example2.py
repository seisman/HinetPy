import os
from datetime import timedelta

from HinetPy import Client, win32
from obspy import UTCDateTime
from obspy.clients.fdsn import Client as fdsnClient

fdsnclient = fdsnClient("IRIS")
starttime = UTCDateTime("2005-01-01")
endtime = UTCDateTime("2005-01-03")
catalog = fdsnclient.get_events(
    starttime=starttime, endtime=endtime, minmagnitude=6, catalog="ISC"
)

client = Client("username", "password")
for event in catalog:  # loop over events
    origin = event.origins[0].time.datetime
    starttime = origin + timedelta(hours=9)  # deal with TimeZone issue
    outdir = origin.strftime("%Y%m%d%H%M")

    # skip if outdir already exists to avoid overwrite
    if os.path.exits(outdir):
        continue

    data, ctable = client.get_continuous_waveform("0101", starttime, 20, outdir=outdir)
    win32.extract_sac(data, ctable, outdir=outdir, with_pz=True)
