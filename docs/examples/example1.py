import csv
import os
from datetime import datetime, timedelta

from HinetPy import Client, win32

client = Client("username", "password")
with open("events.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter="|")
    reader.fieldnames = [field.strip() for field in reader.fieldnames]
    for row in reader:  # loop over events
        origin = datetime.strptime(row["Time"], "%Y-%m-%dT%H:%M:%S")
        starttime = origin + timedelta(hours=9)  # deal with TimeZone issue
        outdir = origin.strftime("%Y%m%d%H%M")

        # skip if outdir already exists to avoid overwrite
        if os.path.exists(outdir):
            continue

        data, ctable = client.get_continuous_waveform(
            "0101", starttime, 20, outdir=outdir
        )
        win32.extract_sac(data, ctable, outdir=outdir, with_sacpz=True)
