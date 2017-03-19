#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime

import pytest
import requests

from HinetPy import Client
from datetime import datetime

username = "test_username"
password = "test_password"

client = Client(username, password)
client.select_stations('0101', ['N.AAKH', 'N.ABNH'])


class TestClientCheckClass:
    def test_check_service_update(self):
        assert not client.check_service_update()

    def test_check_package_release(self):
        assert not client.check_package_release()

    def test_check_cmd_exists(self):
        assert client.check_cmd_exists()


class TestGetwaveformClass:
    def test_get_waveform_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        data, ctable = client.get_waveform('0101', starttime, 10)

        assert data == '0101_201001010000_10.cnt'
        assert os.path.exists(data)
        os.remove(data)
        assert ctable == '0101_20100101.ch'
        assert os.path.exists(ctable)
        os.remove(ctable)

    def test_get_waveform_custom_name_1(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        data, ctable = client.get_waveform('0101', starttime, 1,
                                           data="customname1.cnt",
                                           ctable="customname1.ch")

        assert data == 'customname1.cnt'
        assert os.path.exists(data)
        os.remove(data)
        assert ctable == 'customname1.ch'
        assert os.path.exists(ctable)
        os.remove(ctable)

    def test_get_waveform_custom_name_2(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        data, ctable = client.get_waveform('0101', starttime, 1,
                                           data="customname2/customname2.cnt",
                                           ctable="customname2/customname2.ch")

        assert data == 'customname2/customname2.cnt'
        assert os.path.exists(data)
        assert ctable == 'customname2/customname2.ch'
        assert os.path.exists(ctable)
        shutil.rmtree("customname2")

    def test_get_waveform_custom_name_3(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        data, ctable = client.get_waveform('0101', starttime, 1,
                                           outdir="customname3")

        assert data == "customname3/0101_201001010000_1.cnt"
        assert os.path.exists(data)
        assert ctable == "customname3/0101_20100101.ch"
        assert os.path.exists(ctable)
        shutil.rmtree("customname3")

    def test_get_waveform_custom_name_4(self):
        starttime = datetime(2010, 1, 1, 0, 0)
        data, ctable = client.get_waveform('0101', starttime, 1,
                                           data="customname4-cnt/test.cnt",
                                           ctable="customname4-ch/test.ch",
                                           outdir="customname4-data")

        assert data == "customname4-cnt/test.cnt"
        assert os.path.exists(data)
        assert ctable == "customname4-ch/test.ch"
        assert os.path.exists(ctable)
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


class TestGetCatalogClass:
    def test_get_arrivaltime_1(self):
        data = client.get_arrivaltime(startdate, 5)
        assert data == 'measure_20100101_5.txt'
        assert os.path.exists(data)
        os.remove(data)

    def test_get_arrivaltime_2(self):
        data = client.get_arrivaltime(startdate, 5, filename="arrivaltime.txt")
        assert data == "arrivaltime.txt"
        assert os.path.exists(data)
        os.remove(data)

    def test_get_focalmechanism_1(self):
        data = client.get_focalmechanism(startdate, 5)
        assert data == 'focal_20100101_5.txt'
        assert os.path.exists(data)
        os.remove(data)

    def test_get_focalmachanism_2(self):
        data = client.get_focalmechanism(startdate, 5, filename="focal.txt")
        assert data == "focalmechanism.txt"
        assert os.path.exists(data)
        os.remove(data)


class TestClientOthersClass:
    def test_parse_code(self):
        assert client._parse_code('0101') = ('01', '01', None)
        assert client._parse_code('0103A') = ('01', '03A', None)
        assert client._parse_code('010503') = ('01', '05', '010503')
        assert client._parse_code('030201') = ('03', '02', '030201')

        with pytest.raise(ValueError):
            client._parse_code('01013')


