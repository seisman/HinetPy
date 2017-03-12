#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from HinetPy import Client

client = Client("test_username", "test_password")
client._get_win32tools()
