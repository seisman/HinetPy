"""
Utility functions used in HinetPy.
"""
import math
import shutil
from datetime import date, datetime
from distutils.version import LooseVersion

import requests
from pkg_resources import get_distribution


def split_integer(number, maxn):
    """
    Split an integer into evenly sized chunks.

    Parameters
    ----------
    number: int
        An interger that to be split into chunks.
    maxn: int
        The maximum number in each chunk.

    Returns
    -------
    chunks: list
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
    latitude,
    longitude,
    minlatitude=-90,
    maxlatitude=90,
    minlongitude=0,
    maxlongitude=360,
):
    """
    Check if a point is inside a box region.

    Parameters
    ----------
    latitude: float
        Latitude of the point.
    longitude: float
        Longitude of the point.
    minlatitude: float
        Minimum latitude of the box region.
    maxlatitude: float
        Maximum latitude of the box region.
    minlongitude: float
        Minimum latitude of the box region.
    maxlongitude: float
        Maximum latitude of the box region.

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
    # Convert longitude to 0-360 range
    longitude = longitude + 360.0 if longitude < 0 else longitude
    if (
        minlatitude <= latitude <= maxlatitude
        and minlongitude <= longitude <= maxlongitude
    ):
        return True
    return False


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) using haversine formula.

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
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * math.asin(math.sqrt(delta)) * 180.0 / math.pi


def point_inside_circular(lat1, lon1, lat2, lon2, minradius=0.0, maxradius=360.0):
    """
    Check if a point is inside a circular region.

    Parameters
    ----------
    lat1: float
        Latitude of the first point.
    lon1: float
        Longitude of the first point.
    lat2: float
        Latitude of the second point.
    lon2: float
        Longitude of the second point.
    minradius: float
        Minimum radius in degrees.
    maxradiuse: float
        Maximum radius in degrees.

    Returns
    -------
    bool:
        True if the point is inside the circular region.

    Examples
    --------
    >>> point_inside_circular(30, 50, 30, 52, 0, 5)
    True
    """
    radius = haversine(lat1, lon1, lat2, lon2)
    if minradius <= radius <= maxradius:
        return True
    return False


def to_datetime(value):
    """Convert a string to datetime in a hard way.

    Parameters
    ----------
    value: str
        A datetime in string format.

    Returns
    -------
    datetime.datetime:
        A datetime in datetime format.

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
    value = value.replace("T", " ")
    value = value.replace("-", " ")
    value = value.replace(":", " ")
    value = value.replace(",", " ")
    value = value.replace("_", " ")

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
        if "." in value:
            strfmt = "%Y %m %d %H %M %S.%f"
        else:
            strfmt = "%Y %m %d %H %M %S"

    return datetime.strptime(value, strfmt)


def check_cmd_exists():
    """
    Check if ``catwin32`` and ``win2sac_32`` from win32tools are in PATH.

    It reports errors if ``catwin32`` and/or ``win2sac_32`` are NOT found in PATH.
    In this case, please download win32tools from
    `Hi-net <http://www.hinet.bosai.go.jp/>`_
    and make sure both binary files are in your PATH.
    """
    error = 0
    for cmd in ["catwin32", "win2sac_32"]:
        fullpath = shutil.which(cmd)
        if fullpath:
            print(f"{cmd}: {fullpath}")
        else:
            error += 1
            print(f"{cmd}: not found in PATH.")
    return not bool(error)


def check_package_release():
    """
    Check whether HinetPy has a new release.
    """
    url = "https://pypi.python.org/pypi/HinetPy/json"
    res = requests.get(url)
    if res.status_code != 200:
        print("Error in connecting PyPI. Skipped.")
        return False
    latest_release = res.json()["info"]["version"]

    current_version = f'{get_distribution("HinetPy").version}'
    if LooseVersion(latest_release) > LooseVersion(current_version):
        print(f"HinetPy v{latest_release} is released. See {url} for details.")
        return True

    print(f"You're using the latest version (v{current_version}).")
    return False
