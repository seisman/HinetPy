#!/usr/bin/env python
# -*- coding: utf-8 -*-

username = "test_username"
password = "test_password"

import os
import shutil
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

class TestGetwaveformClass:
    def test_get_waveform_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 10)

        assert win32 == '0101_201001010000_10.cnt'
        assert os.path.exists(win32)
        os.remove(win32)
        assert chfile == '0101_20100101.ch'
        assert os.path.exists(chfile)
        os.remove(chfile)

    def test_get_waveform_custom_name_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1,
                                            data="customname1.cnt",
                                            ctable="customname1.ch")

        assert win32 == 'customname1.cnt'
        assert os.path.exists(win32)
        os.remove(win32)
        assert chfile == 'customname1.ch'
        assert os.path.exists(chfile)
        os.remove(chfile)

    def test_get_waveform_custom_name_2(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1,
                                            data="customname2/customname2.cnt",
                                            ctable="customname2/customname2.ch")

        assert win32 == 'customname2/customname2.cnt'
        assert os.path.exists(win32)
        assert chfile == 'customname2/customname2.ch'
        assert os.path.exists(chfile)
        shutil.rmtree("customname2")

    def test_get_waveform_custom_name_3(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1,
                                            outdir="customname3")

        assert win32 == "customname3/0101_201001010000_1.cnt"
        assert os.path.exists(win32)
        assert chfile == "customname3/0101_20100101.ch"
        assert os.path.exists(chfile)
        shutil.rmtree("customname3")

    def test_get_waveform_custom_name_4(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        win32, chfile = client.get_waveform('0101', starttime, 1,
                                            data="customname4-cnt/test.cnt",
                                            ctable="customname4-ch/test.ch",
                                            outdir="customname4-data")

        assert win32 == "customname4-cnt/test.cnt"
        assert os.path.exists(win32)
        assert chfile == "customname4-ch/test.ch"
        assert os.path.exists(chfile)
        shutil.rmtree("customname4-cnt")
        shutil.rmtree("customname4-ch")


class TestGetwaveformSpanClass:
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

