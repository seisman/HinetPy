#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check if a network has more channels"""

from datetime import datetime, timedelta

from HinetPy import Client
from HinetPy.header import NETWORK
from HinetPy.win32 import _get_channels


username = "test_username"
password = "test_password"
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
