#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

subprocess.call(['../ch2pz.py', '201001010000'])
subprocess.call(['../ch2pz.py', '201101010000', '-C', 'U'])
subprocess.call(['../ch2pz.py', '201101010000', '-D', 'ch2pz-test'])
subprocess.call(['../ch2pz.py', '201101010000', '-D', 'ch2pz-test', '-S', '.PZ'])
