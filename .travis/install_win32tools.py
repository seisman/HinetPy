#!/usr/bin/env python

import os
import tarfile

from HinetPy import Client

username = "test_username"
password = "test_password"

client = Client(username, password)
client._get_win32tools()

with tarfile.open("win32tools.tar.gz") as tar:
    tar.extractall()

os.chdir("win32tools")
os.system("make")
os.mkdir("bin")
os.rename("catwin32.src/catwin32", "bin/catwin32")
os.rename("win2sac.src/win2sac_32", "bin/win2sac_32")
