"""
Tests for win32.py
"""
import filecmp
import glob
import os
import shutil
import uuid

import pytest
from HinetPy import Client, win32

username = os.environ["HINET_USERNAME"]
password = os.environ["HINET_PASSWORD"]

TESTDIR = "testdir-" + str(uuid.uuid4())
path = os.path.join(TESTDIR, "data")
data = os.path.join(path, "0101_201701010000_3.cnt")
ctable = os.path.join(path, "0101_20170101.ch")


@pytest.fixture(scope="module", autouse=True)
def get_test_data():
    """
    Download the test data used in the tests.
    """
    client = Client(username, password)
    client.select_stations("0101", ["N.NGUH", "N.NNMH"])
    client.get_continuous_waveform(
        "0101", "2017-01-01T00:00", 3, outdir=path, cleanup=False
    )
    for file in glob.glob("20170101000?0101VM.cnt"):
        os.rename(file, os.path.join(path, file))


def test_extract_sac_defaults():
    """
    Extract SAC files using default settings.
    """
    outdir = os.path.join(TESTDIR, "test_extract_sac_defaults")
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


def test_extract_sac_without_suffix():
    """
    Extract SAC files without the "SAC" suffix.
    """
    outdir = os.path.join(TESTDIR, "test_extract_sac_without_suffix")
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


def test_extract_sac_filter_by_ids():
    """
    Extract SAC files by filtering channels using IDs.
    """
    outdir = os.path.join(TESTDIR, "test_extract_sac_filter_by_ids")
    win32.extract_sac(data, ctable, filter_by_id="3e8?", outdir=outdir)
    sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
    filelist = ["N.NNMH.E.SAC", "N.NNMH.N.SAC", "N.NNMH.U.SAC"]
    sac_to_check = [os.path.join(outdir, name) for name in filelist]
    assert sac == sac_to_check


def test_extract_sac_filter_by_name():
    """
    Extract SAC files by filtering channels using names.
    """
    outdir = os.path.join(TESTDIR, "test_extract_sac_filter_by_name")
    win32.extract_sac(data, ctable, filter_by_name="N.NG*", outdir=outdir)
    sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
    filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NGUH.U.SAC"]
    sac_to_check = [os.path.join(outdir, name) for name in filelist]
    assert sac == sac_to_check


def test_extract_sac_filter_by_component():
    """
    Extract SAC files by filtering channels using component names.
    """
    outdir = os.path.join(TESTDIR, "test_extract_sac_filter_by_component")
    win32.extract_sac(data, ctable, filter_by_component=["N", "E"], outdir=outdir)
    sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
    filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NNMH.E.SAC", "N.NNMH.N.SAC"]
    sac_to_check = [os.path.join(outdir, name) for name in filelist]
    assert sac == sac_to_check


def test_extract_sac_with_polezero():
    """
    Extract SAC files and polezero files.
    """
    outdir = os.path.join(TESTDIR, "test6")
    win32.extract_sac(
        data, ctable, filter_by_component=["N", "E"], outdir=outdir, with_sacpz=True
    )
    sac = sorted(glob.glob(os.path.join(outdir, "N.*.SAC")))
    filelist = ["N.NGUH.E.SAC", "N.NGUH.N.SAC", "N.NNMH.E.SAC", "N.NNMH.N.SAC"]
    sac_to_check = [os.path.join(outdir, name) for name in filelist]
    assert sac == sac_to_check

    filelist = [
        "N.NGUH.E.SAC_PZ",
        "N.NGUH.N.SAC_PZ",
        "N.NNMH.E.SAC_PZ",
        "N.NNMH.N.SAC_PZ",
    ]
    pz_to_check = [os.path.join(outdir, name) for name in filelist]
    assert pz_to_check == sorted(glob.glob(os.path.join(outdir, "N.*.SAC_PZ")))


def test_extract_sac_none_input():
    """
    Return nothing if the inputs are None.
    """
    assert win32.extract_sac(None, None) is None


def test_extract_pz_default():
    """
    Extract SAC PZ files using default settings.
    """
    outdir = os.path.join(TESTDIR, "ch1")
    win32.extract_pz(ctable, outdir=outdir)
    pz_to_check = [
        "N.NNMH.U.SAC_PZ",
        "N.NNMH.N.SAC_PZ",
        "N.NNMH.E.SAC_PZ",
        "N.NGUH.U.SAC_PZ",
        "N.NGUH.N.SAC_PZ",
        "N.NGUH.E.SAC_PZ",
    ]
    assert sorted(os.listdir(outdir)) == sorted(pz_to_check)


def test_extract_pz_custom_suffix():
    """
    Extract SAC PZ files using custom suffix.
    """
    outdir = os.path.join(TESTDIR, "ch2")
    win32.extract_pz(ctable, suffix="SACPZ", outdir=outdir, keep_sensitivity=True)
    pz_to_check = [
        "N.NNMH.U.SACPZ",
        "N.NNMH.N.SACPZ",
        "N.NNMH.E.SACPZ",
        "N.NGUH.U.SACPZ",
        "N.NGUH.N.SACPZ",
        "N.NGUH.E.SACPZ",
    ]
    assert sorted(os.listdir(outdir)) == sorted(pz_to_check)


def test_extract_pz_filter_by_component():
    """
    Extract SAC PZ files by filtering channels using components.
    """
    outdir = os.path.join(TESTDIR, "ch3")
    win32.extract_pz(ctable, filter_by_component="U", outdir=outdir)
    pz_to_check = ["N.NNMH.U.SAC_PZ", "N.NGUH.U.SAC_PZ"]
    assert sorted(os.listdir(outdir)) == sorted(pz_to_check)


def test_extract_pz_non_input():
    """
    Return None if the input is None.
    """


def test_merge_without_sort():
    """
    Merge win32 files without sorting files.
    """
    datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
    final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
    total_data = "test_merge_without_sort.cnt"

    win32.merge(datas, total_data)
    assert os.path.exists(total_data)
    assert filecmp.cmp(total_data, final_to_check)
    os.unlink(total_data)


def test_merge_with_sort():
    """
    Merge win32 files that are forced to be sorted.
    """
    # datas is unsorted
    datas = glob.glob(os.path.join(path, "20170101000?0101VM.cnt"))[::-1]
    final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
    total_data = "test_merge_with_sort.cnt"

    win32.merge(datas, total_data, force_sort=True)
    assert os.path.exists(total_data)
    assert filecmp.cmp(total_data, final_to_check)
    os.unlink(total_data)


def test_merge_with_deep_level_directory():
    """
    Output the merged win32 data to a deep directory.
    """
    datas = sorted(glob.glob(os.path.join(path, "20170101000?0101VM.cnt")))
    final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
    total_data = "test_merge/with/deep/level/directory/output.cnt"

    win32.merge(datas, total_data)
    assert os.path.exists(total_data)
    assert filecmp.cmp(total_data, final_to_check)
    shutil.rmtree("test_merge")


def test_merge_with_wildcard():
    """
    Merge files specified by a wildcard.
    """
    final_to_check = os.path.join(path, "0101_201701010000_3.cnt")
    total_data = "test_merge_with_wildcard.cnt"

    datas = os.path.join(path, "20170101000?0101VM.cnt")
    win32.merge(datas, total_data)
    assert os.path.exists(total_data)
    assert filecmp.cmp(total_data, final_to_check)
    os.unlink(total_data)


def test_merge_not_a_valid_wildcard():
    """
    Should raise a warning if the wildcard finds nothing.
    """
    datas = os.path.join(path, "not-a-valid-wildcard.cnt")
    total_data = "test_merge_not_a_valid_wildcard.cnt"
    with pytest.raises(FileNotFoundError):
        win32.merge(datas, total_data)
