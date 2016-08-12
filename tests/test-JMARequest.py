#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

subprocess.call(['../HinetJMARequest.py', '--measure', '20100101', '1'])
subprocess.call(['../HinetJMARequest.py', '--measure', '20100101', '7'])
subprocess.call(['../HinetJMARequest.py', '--measure', '20100101', '10'])
subprocess.call(['../HinetJMARequest.py', '--mecha', '20100101', '1'])
subprocess.call(['../HinetJMARequest.py', '--mecha', '20100101', '7'])
subprocess.call(['../HinetJMARequest.py', '--mecha', '20100101', '10'])
