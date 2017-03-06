#!/usr/bin/env python
# -*- coding: utf-8 -*-

username = "username"
password = "password"

import os
from datetime import datetime

import pytest
import requests

from HinetPy import Client
from HinetPy.header import network
from datetime import datetime

client = Client(username, password)
client.select_stations('0101', ['N.AAKH', 'N.ABNH'])

class TestClass:
    def test_check_service_update(self):
        assert client.check_service_update() == False

    def test_check_module_release(self):
        assert client.check_module_release() == False

    def test_check_cmd_exists(self):
        assert client.check_cmd_exists() == True

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
        win32, chfile = client.get_waveform('0101', starttime, 1, win32_filename="test.cnt", channeltable_filename="test.ch")

        assert (win32, chfile) == ("test.cnt", "test.ch")

    def test_get_waveform_custom_name_2(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, win32_filename="data/test.cnt", channeltable_filename="ch/test.ch")

        assert os.path.exists("data/test.cnt")
        assert os.path.exists("ch/test.ch")

    def test_get_waveform_custom_name_3(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, output_directory="data")

        assert os.path.exists("data/0101_201001010000_1.cnt")
        assert os.path.exists("data/0101_20100101.ch")

    def test_get_waveform_custom_name_4(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1, win32_filename="cnt/test.cnt", channeltable_filename="ch/test.ch", output_directory="data")

        assert os.path.exists("cnt/test.cnt")
        assert os.path.exists("ch/test.ch")
