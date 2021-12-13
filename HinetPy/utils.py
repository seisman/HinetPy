"""
Utility functions used by HinetPy.
"""
import math
from datetime import date, datetime


def split_integer(number, maxn):
    """
    Split an integer into evenly sized chunks.

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
    minlatitude=None,
    maxlatitude=None,
    minlongitude=None,
    maxlongitude=None,
):
    """
    Check if a point inside a box region.

    >>> point_inside_box(40, 130)
    True
    >>> point_inside_box(40, 130, 0, 50, 100, 150)
    True
    >>> point_inside_box(40, 130, 0, 30, 100, 150)
    False
    >>> point_inside_box(40, 130, None, 50, 100, None)
    True
    """
    if minlatitude and latitude < minlatitude:
        return False
    if maxlatitude and latitude > maxlatitude:
        return False
    if minlongitude and longitude < minlongitude:
        return False
    if maxlongitude and longitude > maxlongitude:
        return False
    return True


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) using haversine formula.

    see https://stackoverflow.com/a/4913653/7770208

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
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return c * 180.0 / math.pi


def point_inside_circular(lat1, lon1, lat2, lon2, minradius=None, maxradius=None):
    """
    Check if a point inside a circular region.

    >>> point_inside_circular(30, 50, 30, 52, 0, 5)
    True
    """
    radius = haversine(lat1, lon1, lat2, lon2)
    if minradius and radius < minradius:
        return False
    if maxradius and radius > maxradius:
        return False
    return True


def to_datetime(value):
    """Convert to datetime in a hard way.

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
