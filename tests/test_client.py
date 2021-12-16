import os
import shutil
from datetime import date, datetime

import pytest
import requests
from HinetPy import Client

username = os.environ["HINET_USERNAME"]
password = os.environ["HINET_PASSWORD"]


@pytest.fixture(scope="module")
def client():
    client = Client(username, password)
    client.select_stations("0101", ["N.AAKH", "N.ABNH"])
    yield client
    client.select_stations("0101")


def test_client_init_and_login_succeed():
    Client(username, password)


def test_client_init_and_login_fail():
    """Raise ConnectionError if requests fails."""
    with pytest.raises(requests.ConnectionError):
        Client("anonymous", "anonymous")


def test_login_after_init():
    client = Client()
    client.login(username, password)


def test_check_service_update(client):
    assert not client.check_service_update()


def test_check_package_release(client):
    assert not client.check_package_release()


def test_check_cmd_exists(client):
    assert client.check_cmd_exists()


def test_docter(client):
    client.doctor()


def test_get_continuous_waveform_1(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform("0101", starttime, 9)

    assert data == "0101_201001010000_9.cnt"
    assert os.path.exists(data)
    os.remove(data)
    assert ctable == "0101_20100101.ch"
    assert os.path.exists(ctable)
    os.remove(ctable)


def test_get_continuous_waveform_starttime_in_string(client):
    data, ctable = client.get_continuous_waveform("0101", "2010-01-01T00:00", 9)

    assert data == "0101_201001010000_9.cnt"
    assert os.path.exists(data)
    os.remove(data)
    assert ctable == "0101_20100101.ch"
    assert os.path.exists(ctable)
    os.remove(ctable)


def test_get_continuous_waveform_custom_name_1(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform(
        "0101", starttime, 1, data="customname1.cnt", ctable="customname1.ch"
    )

    assert data == "customname1.cnt"
    assert os.path.exists(data)
    os.remove(data)
    assert ctable == "customname1.ch"
    assert os.path.exists(ctable)
    os.remove(ctable)


def test_get_continuous_waveform_custom_name_2(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform(
        "0101",
        starttime,
        1,
        data="customname2/customname2.cnt",
        ctable="customname2/customname2.ch",
    )

    assert data == "customname2/customname2.cnt"
    assert os.path.exists(data)
    assert ctable == "customname2/customname2.ch"
    assert os.path.exists(ctable)
    shutil.rmtree("customname2")


def test_get_continuous_waveform_custom_name_3(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform(
        "0101", starttime, 1, outdir="customname3"
    )

    assert data == "customname3/0101_201001010000_1.cnt"
    assert os.path.exists(data)
    assert ctable == "customname3/0101_20100101.ch"
    assert os.path.exists(ctable)
    shutil.rmtree("customname3")


def test_get_continuous_waveform_custom_name_4(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform(
        "0101",
        starttime,
        1,
        data="customname4-cnt/test.cnt",
        ctable="customname4-ch/test.ch",
        outdir="customname4-data",
    )

    assert data == "customname4-cnt/test.cnt"
    assert os.path.exists(data)
    assert ctable == "customname4-ch/test.ch"
    assert os.path.exists(ctable)
    shutil.rmtree("customname4-cnt")
    shutil.rmtree("customname4-ch")


def test_get_waveform_alias(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_waveform("0101", starttime, 1)


def test_get_continuous_waveform_wrong_span_1(client):
    starttime = datetime(2005, 1, 1, 0, 0)
    with pytest.raises(ValueError):
        client.get_continuous_waveform("0101", starttime, 0)


def test_get_continuous_waveform_wrong_span_2(client):
    starttime = datetime(2005, 1, 1, 0, 0)
    with pytest.raises(ValueError):
        client.get_continuous_waveform("0101", starttime, -4)


def test_get_continuous_waveform_wrong_span_3(client):
    starttime = datetime(2005, 1, 1, 0, 0)
    with pytest.raises(TypeError):
        client.get_continuous_waveform("0101", starttime, 2.5)


def test_get_continuous_waveform_span_larger_than_int(client):
    starttime = datetime(2005, 1, 1, 0, 0)
    with pytest.raises(ValueError):
        client.get_continuous_waveform("0101", starttime, 400000)


def test_get_continuous_waveform_larger_max_span(client):
    starttime = datetime(2010, 1, 1, 0, 0)
    data, ctable = client.get_continuous_waveform("0101", starttime, 10, max_span=65)
    assert data == "0101_201001010000_10.cnt"
    assert os.path.exists(data)
    os.remove(data)
    assert ctable == "0101_20100101.ch"
    assert os.path.exists(ctable)
    os.remove(ctable)


def test_get_continuous_waveform_wrong_starttime(client):
    starttime = datetime(2001, 1, 1, 0, 0)
    with pytest.raises(ValueError):
        client.get_continuous_waveform("0101", starttime, 1)


def test_get_arrivaltime_1(client):
    startdate = date(2010, 1, 1)
    data = client.get_arrivaltime(startdate, 5)
    assert data == "measure_20100101_5.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_arrivaltime_2(client):
    startdate = date(2010, 1, 1)
    data = client.get_arrivaltime(startdate, 5, filename="arrivaltime.txt")
    assert data == "arrivaltime.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_arrivaltime_use_datetime(client):
    startdate = datetime(2010, 1, 1)
    data = client.get_arrivaltime(startdate, 5)
    assert data == "measure_20100101_5.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_arrivaltime_startdate_in_string(client):
    data = client.get_arrivaltime("20100101", 5)
    assert data == "measure_20100101_5.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_focalmechanism_1(client):
    startdate = date(2010, 1, 1)
    data = client.get_focalmechanism(startdate, 5)
    assert data == "mecha_20100101_5.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_focalmachanism_2(client):
    startdate = date(2010, 1, 1)
    data = client.get_focalmechanism(startdate, 5, filename="focal.txt")
    assert data == "focal.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_focalmachanism_use_datetime(client):
    startdate = datetime(2010, 1, 1)
    data = client.get_focalmechanism(startdate, 5, filename="focal.txt")
    assert data == "focal.txt"
    assert os.path.exists(data)
    os.remove(data)


def test_get_catalog_wrong_span(client):
    startdate = date(2010, 1, 1)
    with pytest.raises(ValueError):
        client.get_arrivaltime(startdate, 10)


def test_get_event_waveform(client):
    client.get_event_waveform(
        "201001010000",
        "201001020000",
        minmagnitude=3.5,
        maxmagnitude=5.5,
        mindepth=0,
        maxdepth=70,
        minlatitude=40.0,
        minlongitude=140.0,
        latitude=46.49,
        longitude=151.97,
        maxradius=1.0,
    )
    assert os.path.exists("D20100101000189_20/D20100101000189_20.evt")
    shutil.rmtree("D20100101000189_20")


def test_get_station_list(client):
    stations = client.get_station_list("0101")
    assert type(stations) == list
    assert len(stations) >= 700

    stations = client.get_station_list("0120")
    assert type(stations) == list
    assert len(stations) >= 120

    stations = client.get_station_list("0131")
    assert type(stations) == list
    assert len(stations) >= 250


def test_get_allowed_span(client):
    assert client._get_allowed_span("0401") == 60
    client.select_stations("0101")
    assert client._get_allowed_span("0101") == 5
    client.select_stations("0101", ["N.AAKH", "N.ABNH"])
    assert client._get_allowed_span("0101") == 60


def test_get_selected_stations(client):
    client.get_selected_stations("0101")
    client.get_selected_stations("0103")
    with pytest.raises(ValueError):
        client.get_selected_stations("0501")


def test_get_win32tools(client):
    assert client._get_win32tools() == "win32tools.tar.gz"
    os.remove("win32tools.tar.gz")
