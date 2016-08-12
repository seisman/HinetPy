#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

def test1():
    print("#1. rdhinet.py dirname")
    subprocess.call(['../rdhinet.py', '201001010000'])

def test2():
    print("#2. rdhinet.py dirname -C E,N")
    subprocess.call(['../rdhinet.py', '201001010000', '-C', 'E,N'])

def test3():
    print("#3. rdhinet.py dirname -D abc")
    subprocess.call(['../rdhinet.py', '201001010000', '-D', 'abc'])

def test4():
    print("#4. rdhinet.py dirname -S SAC")
    subprocess.call(['../rdhinet.py', '201001010000', '-S', 'sac'])

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
