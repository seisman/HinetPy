#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pytest
import requests

from HinetPy import Client
from HinetPy.header import network
from HinetPy.win32 import _get_channels

username = "username"
password = "password"
client = Client(username, password)

class TestClass:
    def test_number_of_channels(self):
        """Check if a network has more channel
        """
        difference = {}
        # always set one day before today as starttime
        starttime = datetime.today() - timedelta(days=1)
        for code in sorted(network.keys()):
            win32, chfile = client.get_waveform(code, starttime, 1)
            count = len(_get_channels(chfile))

            if count > network[code].channels:  # more
                difference[code] = count

        for code in difference.keys():
            print(code, difference[code])

        assert len(difference) == 0
