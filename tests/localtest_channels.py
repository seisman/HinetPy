"""
Check the number of channels for each network.
"""

import os
from datetime import datetime, timedelta

from HinetPy import Client
from HinetPy.header import NETWORK
from HinetPy.win32 import read_ctable

username = os.environ["HINET_USERNAME"]
password = os.environ["HINET_PASSWORD"]
client = Client(username, password)

# always set one day before today as starttime
starttime = datetime.today() - timedelta(days=1)
for code in sorted(NETWORK.keys()):
    win32, chfile = client.get_continuous_waveform(code, starttime, 1)
    if chfile is None:
        continue
    count = len(read_ctable(chfile))
    print(code, count)
