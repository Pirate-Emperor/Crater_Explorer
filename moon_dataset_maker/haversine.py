import math


def haversine(latitude_A, longitude_A, latitude_B, longitude_B):
    """
    Calculate the real distance between two location on Moon, using
    the latitude and longtitude infomation.

    Parameters
    ----------
    latitude_A: float
        latitude of first location
    longitude_A: float
        longitude of first location
    latitude_B: float
        latitude of second location
    longitude_B: float
        longitude of second location

    Returns
    ----------
    distance: float
        distance in km

    Examples
    --------
    >>> haversine(20, 40, 40, 50)
    659.7813940573243

    """
    dLat = (latitude_B - latitude_A) * math.pi / 180.0
    dLon = (longitude_B - longitude_A) * math.pi / 180.0

    latitude_A = (latitude_A) * math.pi / 180.0
    latitude_B = (latitude_B) * math.pi / 180.0
    a = pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(
        latitude_A
    ) * math.cos(latitude_B)
    radius = 3474.8 / 2
    c = 2 * math.asin(math.sqrt(a))
    distance = radius * c
    return distance
