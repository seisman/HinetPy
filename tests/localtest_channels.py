"""Check if a network has more channels"""

import os
from datetime import datetime, timedelta

from HinetPy import Client
from HinetPy.header import NETWORK
from HinetPy.win32 import _get_channels

username = os.environ["HINET_USERNAME"]
password = os.environ["HINET_PASSWORD"]
client = Client(username, password)

difference = {}
# always set one day before today as starttime
starttime = datetime.today() - timedelta(days=1)
for code in sorted(NETWORK.keys()):
    win32, chfile = client.get_continuous_waveform(code, starttime, 1)
    count = len(_get_channels(chfile))

    if count > NETWORK[code].channels:  # more
        difference[code] = count

    for code in difference.keys():
        print(code, difference[code])
