#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import pytest

from HinetPy.utils import split_integer, point_inside_box, haversine, \
        point_inside_circular, string2datetime

class TestUtilsClass:
    def test_split_integer(self):
        assert split_integer(16, 4) == [4, 4, 4, 4]
        assert split_integer(15, 4) == [4, 4, 4, 3]
        assert split_integer(14, 4) == [4, 4, 3, 3]
        assert split_integer(13, 4) == [4, 3, 3, 3]
        assert split_integer(12, 4) == [4, 4, 4]

    def test_point_inside_box(self):
        assert point_inside_box(40, 130)
        assert point_inside_box(40, 130, 0, 50, 100, 150)
        assert point_inside_box(40, 130, None, 50, 100, None)
        assert not point_inside_box(40, 130, 50, 80, 100, 150)

    def test_haversine(self):
        assert pytest.approx(haversine(40, 130, 50, 140), 0.01) == 12.22
        assert pytest.approx(haversine(-20, 50, 30, 70), 0.01) == 53.58

    def test_point_inside_circular(self):
        assert point_inside_circular(30, 50, 30, 52, 0, 5)
        assert not point_inside_circular(30, 50, 30, 60, 0, 5)

    def test_string2datetime(self):
        assert string2datetime('20100101') == datetime(2010, 1, 1, 0, 0)
        assert string2datetime('201001010234') == datetime(2010, 1, 1, 2, 34)
        assert string2datetime('2010-01-01') == datetime(2010, 1, 1, 0, 0)
        assert string2datetime('2010-01-01T02:34') == datetime(2010, 1, 1, 2, 34)
