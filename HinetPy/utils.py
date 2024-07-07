"""
Utility functions.
"""

from __future__ import annotations

import math
import shutil
from datetime import date, datetime
from importlib.metadata import version

import requests
from packaging.version import Version


def split_integer(number: int, maxn: int) -> list[int]:
    """
    Split an integer into evenly sized chunks.

    Parameters
    ----------
    number
        An interger that to be split into chunks.
    maxn
        The maximum number in each chunk.

    Returns
    -------
    chunks
        List of integers.

    Examples
    --------
    >>> split_integer(12, 3)
    [3, 3, 3, 3]
    >>> split_integer(15, 4)
    [4, 4, 4, 3]
    """
    count = math.ceil(number / maxn)
    chunks = [number // count for i in range(count)]
    for i in range(number % count):
        chunks[i] += 1
    return chunks


def point_inside_box(
    latitude: float,
    longitude: float,
    minlatitude: float | None = None,
    maxlatitude: float | None = None,
    minlongitude: float | None = None,
    maxlongitude: float | None = None,
) -> bool:
    """
    Check if a point is inside a box region.

    Parameters
    ----------
    latitude
        Latitude of the point.
    longitude
        Longitude of the point.
    minlatitude
        Minimum latitude of the box region.
    maxlatitude
        Maximum latitude of the box region.
    minlongitude
        Minimum longitude of the box region.
    maxlongitude
        Maximum longitude of the box region.

    Returns
    -------
    bool
        True if the point is inside the box region.

    Examples
    --------
    >>> point_inside_box(40, 130)
    True
    >>> point_inside_box(40, 130, 0, 50, 100, 150)
    True
    >>> point_inside_box(40, 130, 0, 30, 100, 150)
    False
    >>> point_inside_box(40, -130, maxlongitude=150)
    False
    >>> point_inside_box(40, -130, maxlongitude=300)
    True
    """
    if (minlongitude and minlongitude < 0.0) or (maxlongitude and maxlongitude < 0.0):
        raise ValueError("minlongitude and maxlongitude should be in 0-360.")
    longitude = longitude + 360.0 if longitude < 0.0 else longitude

    if minlatitude and latitude < minlatitude:
        return False
    if maxlatitude and latitude > maxlatitude:
        return False
    if minlongitude and longitude < minlongitude:
        return False
    return not (maxlongitude and longitude > maxlongitude)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth (specified in
    decimal degrees) using haversine formula.

    Reference: https://stackoverflow.com/a/4913653/7770208.

    >>> haversine(40, 130, 50, 140)
    12.224069629545902
    >>> haversine(-20, 50, 30, 70)
    53.57930271469817
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    delta = (
        math.sin(dlat / 2.0) ** 2.0
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2.0) ** 2.0
    )
    return 2.0 * math.degrees(math.asin(math.sqrt(delta)))


def point_inside_circular(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    minradius: float | None = None,
    maxradius: float | None = None,
) -> bool:
    """
    Check if a point is inside a circular region.

    Parameters
    ----------
    lat1
        Latitude of the point.
    lon1
        Longitude of the point.
    lat2
        Latitude of center of the circular region.
    lon2
        Longitude of center of the circular region.
    minradius
        Minimum radius in degrees of the circular region.
    maxradius
        Maximum radius in degrees of the circular region.

    Returns
    -------
    bool
        True if the point is inside the circular region.

    Examples
    --------
    >>> point_inside_circular(30, 50, 30, 52, 0, 5)
    True
    """
    radius = haversine(lat1, lon1, lat2, lon2)
    return not (
        (minradius and radius < minradius) or (maxradius and radius > maxradius)
    )


def to_datetime(value: str | datetime | date) -> datetime:
    """
    Convert a datetime from :class:`str` to :class:`datetime.datetime` in a hard way.

    Parameters
    ----------
    value
        A :class:`datetime.datetime` object or a datetime string.

    Returns
    -------
    datetime
        A datetime as :class:`datetime.datetime`.

    Examples
    --------
    >>> to_datetime("201001010000")
    datetime.datetime(2010, 1, 1, 0, 0)
    >>> to_datetime("2010-01-01T03:45")
    datetime.datetime(2010, 1, 1, 3, 45)
    """
    # is datetime
    if isinstance(value, datetime):
        return value
    # is date
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    # is a string
    for char in ["T", "-", ":", ",", "_"]:
        value = value.replace(char, " ")

    parts = value.split(" ")
    strfmt = "%Y%m%d%H%M%S"
    if len(parts) == 1:
        if len(value) == 8:
            strfmt = "%Y%m%d"
        elif len(value) == 12:
            strfmt = "%Y%m%d%H%M"
        elif len(value) == 14:
            strfmt = "%Y%m%d%H%M%S"
        elif len(value) > 14:
            strfmt = "%Y%m%d%H%M%S.%f"
    elif len(parts) == 3:
        strfmt = "%Y %m %d"
    elif len(parts) == 5:
        strfmt = "%Y %m %d %H %M"
    elif len(parts) == 6:
        strfmt = "%Y %m %d %H %M %S.%f" if "." in value else "%Y %m %d %H %M %S"

    return datetime.strptime(value, strfmt)


def check_cmd_exists(cmd: str) -> bool:
    """
    Check if a command exists in PATH and is executable.

    Parameters
    ----------
    cmd
        Name of the command.

    Returns
    -------
    bool
        True is the command exists in PATH is executable.
    """
    fullpath = shutil.which(cmd)
    if fullpath:
        print(f"{cmd}: Full path is {fullpath}.")
    else:
        print(f"{cmd}: Not found in PATH or isn't executable.")
    return bool(fullpath)


def check_package_release() -> bool:
    """
    Check whether HinetPy has a new release.

    Returns
    -------
    bool
        True if HinetPy has a new release.
    """
    res = requests.get("https://pypi.org/pypi/HinetPy/json", timeout=30)
    if res.status_code != 200:
        raise requests.HTTPError("Error in connecting to PyPI.")
    latest_release = res.json()["info"]["version"]

    current_version = f'v{version("HinetPy")}'
    if Version(latest_release) > Version(current_version):
        print(
            f"HinetPy v{latest_release} is released. "
            "See https://pypi.org/project/HinetPy/ for details."
        )
        return True

    print(f"You're using the latest version (v{current_version}).")
    return False
