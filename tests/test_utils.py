"""
Tests for utils.py.
"""
from datetime import date, datetime

import pytest
from HinetPy.utils import (
    haversine,
    point_inside_box,
    point_inside_circular,
    split_integer,
    to_datetime,
)


def test_split_integer():
    """
    Test split_integer.
    """
    assert split_integer(16, 4) == [4, 4, 4, 4]
    assert split_integer(15, 4) == [4, 4, 4, 3]
    assert split_integer(14, 4) == [4, 4, 3, 3]
    assert split_integer(13, 4) == [4, 3, 3, 3]
    assert split_integer(12, 4) == [4, 4, 4]


def test_point_inside_box():
    """
    Test point_inside_box.
    """
    assert point_inside_box(40, 130)
    assert point_inside_box(40, 130, 0, 50, 100, 150)
    assert point_inside_box(40, 130, maxlatitude=50, minlongitude=100)
    assert not point_inside_box(40, 130, 50, 80, 100, 150)
    assert not point_inside_box(85, 130, 50, 80, 100, 150)
    assert not point_inside_box(60, 170, 50, 80, 100, 150)


def test_haversine():
    """
    Test haversine.
    """
    assert pytest.approx(haversine(40, 130, 50, 140), 0.01) == 12.22
    assert pytest.approx(haversine(-20, 50, 30, 70), 0.01) == 53.58


def test_point_inside_circular():
    """
    Test point_inside_circular.
    """
    assert point_inside_circular(30, 50, 30, 52, 0, 5)
    assert not point_inside_circular(30, 50, 30, 60, 0, 5)
    assert not point_inside_circular(30, 50, 30, 60, 30, 50)


def test_to_datetime():
    """
    Test to_datetime.
    """
    # pylint: disable=invalid-name
    dt = datetime(2010, 2, 3)
    assert dt == to_datetime(dt)

    dt1 = date(2010, 2, 3)
    dt2 = datetime(2010, 2, 3)
    assert dt2 == to_datetime(dt1)

    dt = datetime(2010, 2, 3)
    assert dt == to_datetime("20100203")
    assert dt == to_datetime("2010-02-03")

    dt = datetime(2001, 2, 3, 4, 5)
    assert dt == to_datetime("200102030405")
    assert dt == to_datetime("2001-02-03T04:05")
    assert dt == to_datetime("2001-02-03 04:05")

    dt = datetime(2001, 2, 3, 4, 5, 6)
    assert dt == to_datetime("20010203040506")
    assert dt == to_datetime("2001-02-03T04:05:06")
    assert dt == to_datetime("2001-02-03 04:05:06")

    dt = datetime(2001, 2, 3, 4, 5, 6, 789000)
    assert dt == to_datetime("20010203040506.789")
    assert dt == to_datetime("2001-02-03T04:05:06.789")
    assert dt == to_datetime("2001-02-03 04:05:06.789")

    with pytest.raises(ValueError):
        to_datetime("2001023040506")
