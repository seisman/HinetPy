#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests with a non-login client."""

import os
import shutil
from datetime import datetime, date

import pytest
import requests

from HinetPy import Client
from HinetPy.client import _string2datetime


# http://docs.pytest.org/en/latest/fixture.html
#@pytest.fixture is better, but pytest prior 2.10 doesn't support
@pytest.yield_fixture(scope="module")
def client():
    client = Client()
    yield client


class TestClientOthersClass:
    def test_parse_code(self, client):
        assert client._parse_code('0101') == ('01', '01', None)
        assert client._parse_code('0103A') == ('01', '03A', None)
        assert client._parse_code('010503') == ('01', '05', '010503')
        assert client._parse_code('030201') == ('03', '02', '030201')

        with pytest.raises(ValueError):
            client._parse_code('01013')

    def test_info(self, client):
        client.info()
        client.info('0101')

    def test_string(self, client):
        print(client)

    def test_get_station_list(self, client):
        client.get_station_list()

    def test_string2datetime(self):
        dt = datetime(2010, 2, 3)
        assert dt == _string2datetime("20100203")
        assert dt == _string2datetime("2010-02-03")

        dt = datetime(2001, 2, 3, 4, 5)
        assert dt == _string2datetime("200102030405")
        assert dt == _string2datetime("2001-02-03T04:05")
        assert dt == _string2datetime("2001-02-03 04:05")

        dt = datetime(2001, 2, 3, 4, 5, 6)
        assert dt == _string2datetime("20010203040506")
        assert dt == _string2datetime("2001-02-03T04:05:06")
        assert dt == _string2datetime("2001-02-03 04:05:06")

        dt = datetime(2001, 2, 3, 4, 5, 6, 789000)
        assert dt == _string2datetime("20010203040506.789")
        assert dt == _string2datetime("2001-02-03T04:05:06.789")
        assert dt == _string2datetime("2001-02-03 04:05:06.789")

        with pytest.raises(ValueError):
            _string2datetime("2001023040506")
