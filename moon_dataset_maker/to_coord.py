import pandas as pd
import numpy as np
from . import haversine


def to_coord(size, location, crators):
    """
    convert index into latitude and longitude according to relative position

    Parameters
    ----------
    size: tuple or array like
        size of image
    location: tuple or array like
        location boundary of the image
    crators: string
        path of txt file containing predicted relative
        location and size of crators

    Returns
    ----------
    pd.DataFrame(info).T: pandas dataframe
        a dataframe containing coordinate and actual size of crators

    """

    h = size[0]
    w = size[1]
    min_lat = location[0]
    max_lat = location[1]
    min_lon = location[2]
    max_lon = location[3]
    degree_per_pixel = (max_lat - min_lat) / h
    crators = np.loadtxt(crators)
    crators = pd.DataFrame(crators)
    df = crators
    df.columns = ["c", "x", "y", "w", "h"]
    x = df["x"].to_numpy()
    y = df["y"].to_numpy()
    w = df["w"].to_numpy()
    h = df["h"].to_numpy()
    lon_x = x * w * degree_per_pixel + min_lon
    lat_x = max_lat - y * h * degree_per_pixel
    l_x = []
    l_y = []
    for i in range(len(lon_x)):
        l_x.append(haversine(lat_x[i], min_lon, lat_x[i], max_lon))
    for i in range(len(lon_x)):
        l_y.append(haversine(min_lat, lon_x[i], max_lat, lon_x[i]))
    l_x = np.array(l_x)
    l_y = np.array(l_y)
    df2 = pd.DataFrame([lon_x, lat_x, l_x, l_y]).T
    return df2
