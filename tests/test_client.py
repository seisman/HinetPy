#!/usr/bin/env python
# -*- coding: utf-8 -*-

username = "test_username"
password = "test_password"

import os
from datetime import datetime

import pytest
import requests

from HinetPy import Client
from datetime import datetime

client = Client(username, password)
client.select_stations('0101', ['N.AAKH', 'N.ABNH'])

class TestClientCheckClass:
    def test_check_service_update(self):
        assert client.check_service_update() == False

    def test_check_package_release(self):
        assert client.check_package_release() == False

    def test_check_cmd_exists(self):
        assert client.check_cmd_exists() == True

class TestGetWaveformClass:
    def test_get_waveform_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 10)
        assert (win32, chfile) == ('0101_201001010000_10.cnt', '0101_20100101.ch')

    def test_get_waveform_wrong_span_1(self):
        starttime = datetime(2005, 1, 1, 0, 0)
        with pytest.raises(ValueError):
            client.get_waveform('0101', starttime, 0)

    def test_get_waveform_wrong_span_2(self):
        starttime = datetime(2005, 1, 1, 0, 0)
        with pytest.raises(ValueError):
            client.get_waveform('0101', starttime, -4)

    def test_get_waveform_wrong_span_3(self):
        starttime = datetime(2005, 1, 1, 0, 0)
        with pytest.raises(TypeError):
            client.get_waveform('0101', starttime, 2.5)

    def test_get_waveform_wrong_span_4(self):
        starttime = datetime(2005, 1, 1, 0, 0)
        with pytest.raises(ValueError):
            client.get_waveform('0101', starttime, 400000)

    def test_get_waveform_wrong_max_span(self):
        starttime = datetime(2005, 1, 1, 0, 0)
        with pytest.raises(ValueError):
            client.get_waveform('0101', starttime, 10, max_span=65)

    def test_get_waveform_custom_name_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, data="test.cnt", ctable="test.ch")

        assert (win32, chfile) == ("test.cnt", "test.ch")

    def test_get_waveform_custom_name_2(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, data="data/test.cnt", ctable="ch/test.ch")

        assert os.path.exists("data/test.cnt")
        assert os.path.exists("ch/test.ch")

    def test_get_waveform_custom_name_3(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, outdir="data")

        assert os.path.exists("data/0101_201001010000_1.cnt")
        assert os.path.exists("data/0101_20100101.ch")

    def test_get_waveform_custom_name_4(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, data="cnt/test.cnt", ctable="ch/test.ch", outdir="data")

        assert os.path.exists("cnt/test.cnt")
        assert os.path.exists("ch/test.ch")
