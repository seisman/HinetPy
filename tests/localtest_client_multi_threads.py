#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HinetPy import Client
from datetime import datetime

username = "username"
password = "password"
client = Client(username, password)
starttime = datetime(2017, 1, 1, 0, 0)
client.get_continuous_waveform('0101', starttime, 20, threads=4)
