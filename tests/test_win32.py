#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import filecmp
import shutil
from multiprocessing import cpu_count

import pytest

from HinetPy import win32

username = "test_username"
password = "test_password"

pwd = os.path.dirname(__file__)
path = os.path.join(pwd, "data")
data = os.path.join(path, "0101_201701010000_3.cnt")
ctable = os.path.join(path, "0101_20170101.ch")


@pytest.fixture(scope="module", autouse=True)
def get_test_data():
    from HinetPy import Client

    client = Client(username, password)
    client.select_stations("0101", ["N.NGUH", "N.NNMH"])
    client.get_continuous_waveform(
        "0101", "2017-01-01T00:00", 3, outdir=path, cleanup=False
    )
    for file in glob.glob("20170101000?0101VM.cnt"):
        os.rename(file, os.path.join(path, file))


class TestWin32ExtractSACClass:
    def test_extract_sac_1(self):
        outdir = os.path.join(pwd, "test1")
        win32.extract_sac(data, ctable, outdir=outdir)
        sac = sorted(glob.glob(os.path.join(outdir, "*.SAC")))
        filelist = [
            "N.NGUH.E.SAC",
            "N.NGUH.N.SAC",
            "N.NGUH.U.SAC",
            "N.NNMH.E.SAC",
            "N.NNMH.N.SAC",
            "N.NNMH.U.SAC",
        ]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check
        shutil.rmtree(outdir)

    def test_extract_sac_2(self):
        outdir = os.path.join(pwd, "test2")
        win32.extract_sac(data, ctable, suffix="", outdir=outdir)
        sac = sorted(glob.glob(os.path.join(outdir, "N.*.[ENU]")))
        filelist = [
            "N.NGUH.E",
            "N.NGUH.N",
            "N.NGUH.U",
            "N.NNMH.E",
            "N.NNMH.N",
            "N.NNMH.U",
        ]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check
        shutil.rmtree(outdir)

    def test_extract_sac_3(self):
        outdir = os.path.join(pwd, "test3")
        win32.extract_sac(data, ctable, filter_by_id="3e8?", outdir=outdir)
        sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
        filelist = ["N.NNMH.E.SAC", "N.NNMH.N.SAC", "N.NNMH.U.SAC"]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check
        shutil.rmtree(outdir)

    def test_extract_sac_4(self):
        outdir = os.path.join(pwd, "test4")
        win32.extract_sac(data, ctable, filter_by_name="N.NG*", outdir=outdir)
        sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
        filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NGUH.U.SAC"]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check
        shutil.rmtree(outdir)

    def test_extract_sac_5(self):
        outdir = os.path.join(pwd, "test5")
        win32.extract_sac(data, ctable, filter_by_component=["N", "E"], outdir=outdir)
        sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
        filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NNMH.E.SAC", "N.NNMH.N.SAC"]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check
        shutil.rmtree(outdir)

    def test_extract_sac_6(self):
        outdir = os.path.join(pwd, "test6")
        win32.extract_sac(
            data, ctable, filter_by_component=["N", "E"], outdir=outdir, with_pz=True
        )
        sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
        filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NNMH.E.SAC", "N.NNMH.N.SAC"]
        sac_to_check = [os.path.join(outdir, name) for name in filelist]
        assert sac == sac_to_check

        pz = sorted(glob.glob(os.path.join(outdir, "N.*.SAC_PZ")))
        filelist = [
            "N.NGUH.E.SAC_PZ",
            "N.NGUH.N.SAC_PZ",
            "N.NNMH.E.SAC_PZ",
            "N.NNMH.N.SAC_PZ",
        ]
        pz_to_check = [os.path.join(outdir, name) for name in filelist]
        assert pz == pz_to_check
        shutil.rmtree(outdir)


    def test_extract_sac_none_input(self):
        assert win32.extract_sac(None, None) == None


class TestWin32ExtractPZClass:
    def test_extract_pz_1(self):
        outdir = os.path.join(pwd, "ch1")
        win32.extract_pz(ctable, outdir=outdir)
        pz_to_check = [
            "N.NNMH.U.SAC_PZ",
            "N.NNMH.N.SAC_PZ",
            "N.NNMH.E.SAC_PZ",
            "N.NGUH.U.SAC_PZ",
            "N.NGUH.N.SAC_PZ",
            "N.NGUH.E.SAC_PZ",
        ]
        pz = os.listdir(outdir)
        assert sorted(pz) == sorted(pz_to_check)
        shutil.rmtree(outdir)

    def test_extract_pz_2(self):
        outdir = os.path.join(pwd, "ch2")
        win32.extract_pz(ctable, suffix="SACPZ", outdir=outdir)
        pz_to_check = [
            "N.NNMH.U.SACPZ",
            "N.NNMH.N.SACPZ",
            "N.NNMH.E.SACPZ",
            "N.NGUH.U.SACPZ",
            "N.NGUH.N.SACPZ",
            "N.NGUH.E.SACPZ",
        ]
        pz = os.listdir(outdir)
        assert sorted(pz) == sorted(pz_to_check)
        shutil.rmtree(outdir)

    def test_extract_pz_3(self):
        outdir = os.path.join(pwd, "ch3")
        win32.extract_pz(ctable, filter_by_component="U", outdir=outdir)
        pz_to_check = ["N.NNMH.U.SAC_PZ", "N.NGUH.U.SAC_PZ"]
        pz = os.listdir(outdir)
        assert sorted(pz) == sorted(pz_to_check)
        shutil.rmtree(outdir)

    def test_extract_pz_non_input(self):
        assert win32.extract_pz(None) == None


class TestWin32MergeClass:
    def test_merge_without_sort(self):
        datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        total_data = "test_merge_without_sort.cnt"

        win32.merge(datas, total_data)
        assert os.path.exists(total_data)
        assert filecmp.cmp(total_data, final_to_check)
        os.unlink(total_data)

    def test_merge_with_sort(self):
        # datas is unsorted
        datas = glob.glob(os.path.join(path, "20170101000?0101VM.cnt"))[::-1]
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        total_data = "test_merge_with_sort.cnt"

        win32.merge(datas, total_data, force_sort=True)
        assert os.path.exists(total_data)
        assert filecmp.cmp(total_data, final_to_check)
        os.unlink(total_data)

    def test_merge_with_deep_level_directory(self):
        datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        total_data = "test_merge/with/deep/level/directory/output.cnt"

        win32.merge(datas, total_data)
        assert os.path.exists(total_data)
        assert filecmp.cmp(total_data, final_to_check)
        shutil.rmtree("test_merge")

    def test_merge_with_wildcard(self):
        final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
        total_data = "test_merge_with_wildcard.cnt"

        datas = os.path.join(path, "20170101000?0101VM.cnt")
        win32.merge(datas, total_data)
        assert os.path.exists(total_data)
        assert filecmp.cmp(total_data, final_to_check)
        os.unlink(total_data)

    def test_merge_not_a_valid_wildcard(self):
        datas = os.path.join(path, "not-a-valid-wildcard.cnt")
        total_data = "test_merge_not_a_valid_wildcard.cnt"
        with pytest.raises(FileNotFoundError)
            win32.merge(datas, total_data)


class TestWin32OthersClass:
    def test_get_processes(self):
        cpus = cpu_count()
        assert win32._get_processes(0) == cpus - 1
        assert win32._get_processes(-5) == cpus - 1
        assert win32._get_processes(1) == 1
