#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import filecmp
from HinetPy import win32

pwd = os.path.dirname(__file__)
path = os.path.join(pwd, 'data')
data = os.path.join(path, "0101_2017031100_2.cnt")
ctable = os.path.join(path, "0101_20170311.ch")

class TestWin32Class:
    def test_extract_sac_1(self):
        outdir = os.path.join(pwd, "test1")
        win32.extract_sac(data, ctable, outdir=outdir)

    def test_extract_sac_2(self):
        outdir = os.path.join(pwd, "test2")
        win32.extract_sac(data, ctable, suffix="", outdir=outdir)

    def test_extract_sac_3(self):
        outdir = os.path.join(pwd, "test3")
        win32.extract_sac(data, ctable, filter_by_id='3e8?', outdir=outdir)

    def test_extract_sac_4(self):
        outdir = os.path.join(pwd, "test4")
        win32.extract_sac(data, ctable, filter_by_name='N.NG*', outdir=outdir)

    def test_extract_sac_5(self):
        outdir = os.path.join(pwd, "test5")
        win32.extract_sac(data, ctable, filter_by_component=['N', 'E'], outdir=outdir)

    def test_extract_sac_6(self):
        outdir = os.path.join(pwd, "test6")
        win32.extract_sac(data, ctable, filter_by_component=['N', 'E'], outdir=outdir, with_pz=True)


    def test_extract_pz_1(self):
        outdir = os.path.join(pwd, "ch1")
        win32.extract_pz(ctable, outdir=outdir)

    def test_extract_pz_2(self):
        outdir = os.path.join(pwd, "ch2")
        win32.extract_pz(ctable, suffix="SACPZ", outdir=outdir)

    def test_extract_pz_3(self):
        outdir = os.path.join(pwd, "ch3")
        win32.extract_pz(ctable, filter_by_component='U', outdir=outdir)

class TestWin32MergeClass:
    def test_merge_without_sort(self):
        datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        final_data = "test_merge_without_sort.cnt"

        win32.merge(datas, final_data)
        assert os.path.exists(final_data)
        assert filecmp.cmp(final_data, final_to_check)
        os.unlink(final_data)

    def test_merge_with_sort(self):
        # datas is unsorted
        datas = glob.glob(os.path.join(path, "20170101000?0101VM.cnt"))[::-1]
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        final_data = "test_merge_with_sort.cnt"

        win32.merge(datas, final_data, force_sort=True)
        assert os.path.exists(final_data)
        assert filecmp.cmp(final_data, final_to_check)
        os.unlink(final_data)

    def test_merge_with_deep_level_directory(self):
        datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        final_data = "test_merge/with/deep/level/directory/output.cnt"

        win32.merge(datas, final_data)
        assert os.path.exists(final_data)
        assert filecmp.cmp(final_data, final_to_check)
        os.unlink(final_data)
