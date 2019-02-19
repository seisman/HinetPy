#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests with a non-login client."""

import os
import shutil
from datetime import datetime, date

import pytest
import requests

from HinetPy import Client
from HinetPy.client import _parse_code
from HinetPy.utils import string2datetime


# http://docs.pytest.org/en/latest/fixture.html
#@pytest.fixture is better, but pytest prior 2.10 doesn't support
@pytest.yield_fixture(scope="module")
def client():
    client = Client()
    yield client


class TestClientOthersClass:
    def test_parse_code(self, client):
        assert _parse_code('0101') == ('01', '01', None)
        assert _parse_code('0103A') == ('01', '03A', None)
        assert _parse_code('010503') == ('01', '05', '010503')
        assert _parse_code('030201') == ('03', '02', '030201')

        with pytest.raises(ValueError):
            _parse_code('01013')

    def test_info(self, client):
        client.info()
        client.info('0101')

    def test_string(self, client):
        print(client)

    def test_get_station_list(self, client):
        stations = client.get_station_list('0101')
        assert type(stations) == list
        assert len(stations) >= 700
