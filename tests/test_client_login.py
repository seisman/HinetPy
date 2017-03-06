#!/usr/bin/env python
# -*- coding: utf-8 -*-

username = "username"
password = "password"

import pytest
import requests
from HinetPy import Client

class TestClass:
    """Login related tests"""
    def test_client_init_and_login_succeed(self):
        client = Client(username, password)

    def test_client_init_and_login_fail(self):
        """ Raise ConnectionError if requests fails. """

        with pytest.raises(requests.ConnectionError):
            client = Client("anonymous", "anonymous")

    def test_login_after_init(self):
        client = Client()
        client.login(username, password)
