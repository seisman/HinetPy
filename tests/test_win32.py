#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HinetPy import win32
class TestClass:

    def test_extract_sac_1(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", outdir="test1")

    def test_extract_sac_2(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", suffix="", outdir="test2")

    def test_extract_sac_3(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", filter_by_id='3e8?', outdir="test3")

    def test_extract_sac_4(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", filter_by_name='N.NG*', outdir="test4")

    def test_extract_sac_5(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", filter_by_component=['N', 'E'], outdir="test5")

    def test_extract_sac_6(self):
        win32.extract_sac("0101_2017031100_2.cnt", "0101_20170311.ch", filter_by_component=['N', 'E'], outdir="test6", with_pz=True)


    def test_extract_pz_1(self):
        win32.extract_pz("0101_20170311.ch", outdir="ch1")

    def test_extract_pz_2(self):
        win32.extract_pz("0101_20170311.ch", suffix="SACPZ", outdir="ch2")

    def test_extract_pz_3(self):
        win32.extract_pz("0101_20170311.ch", outdir="ch3", filter_by_component='U')
