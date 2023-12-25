import random
import pandas as pd

from . import index_degree_convert
from . import haversine


def random_pick(label_path, img, n=100, output="train", name="B", dimension=416 * 2):
    """
    Randomly pick the center of images and generate small images
    and corresponding labels

    Parameters
    ----------
    label_path: string
        path of labels
    img: array
        the entire image
    n: int
        number of images to generate
    output: str
        type if images, choose from train,val and test
    name: str
        name of image
    dimension: int
        dimension the images generated

    Returns
    ----------
    train_folder: list
        list of data
    rain_deg_region: list
        list of coordinate ranges
    center_index: list
        list of picture center index on the map
    label:numpy.array or list of lists
        list of label information of the crater locations on each image

    """

    craters = pd.read_csv(label_path)
    height = img.shape[0]
    width = img.shape[1]

    i_min = dimension // 2
    j_min = dimension // 2
    i_max = height - dimension // 2
    j_max = int(width * 0.8 * 0.8 - dimension // 2)

    train_width = int(width * 0.8 * 0.8)

    if output == "val":
        j_min = dimension // 2 + train_width
        j_max = int(width * 0.8 - dimension // 2)

    if output == "test":
        j_min = int(width * 0.8 + dimension // 2)
        j_max = width - dimension // 2

    train_folder = []
    train_deg_region = []
    center_index = []
    label = []

    for _ in range(n):
        i = random.randint(i_min, i_max)
        j = random.randint(j_min, j_max)

        center = [i, j]
        center_index.append(center)

        top_left = [i - 416, j - 416]
        bot_right = [i + 416, j + 416]

        train_img = img[top_left[0] : bot_right[0], top_left[1] : bot_right[1]]
        deg_top_left = index_degree_convert(top_left, height, width, name=name)
        deg_bot_right = index_degree_convert(bot_right, height, width, name=name)
        min_lat = deg_bot_right[0]
        max_lat = deg_top_left[0]
        min_lon = deg_top_left[1]
        max_lon = deg_bot_right[1]

        craters_ = craters[
            (craters["LON_ELLI_IMG"] <= max_lon)
            & (craters["LON_ELLI_IMG"] >= min_lon)
            & (craters["LAT_ELLI_IMG"] <= max_lat)
            & (craters["LAT_ELLI_IMG"] >= min_lat)
        ]

        if len(craters_) > 0:
            train_folder.append(train_img)
            x = craters_["LON_ELLI_IMG"].tolist()
            y = craters_["LAT_ELLI_IMG"].tolist()
            w = craters_["DIAM_ELLI_MAJOR_IMG"].tolist()
            h = craters_["DIAM_ELLI_MINOR_IMG"].tolist()

            w_ = []
            h_ = []

            for i in range(craters_.shape[0]):
                fractional_w = w[i] / haversine(y[i], min_lon, y[i], max_lon)
                fractional_h = h[i] / haversine(max_lat, x[i], min_lat, x[i])
                w_.append(fractional_w)
                h_.append(fractional_h)

            xx = []
            yy = []

            for i in range(craters_.shape[0]):
                fractional_x = haversine(y[i], x[i], y[i], min_lon) / haversine(
                    y[i], min_lon, y[i], max_lon
                )
                fractional_y = haversine(y[i], x[i], max_lat, x[i]) / haversine(
                    max_lat, x[i], min_lat, x[i]
                )
                xx.append(fractional_x)
                yy.append(fractional_y)

            l_x = []
            l_y = []
            l_w = []
            l_h = []
            for i in range(len(xx)):
                x0 = max(0, xx[i] - 0.5 * w_[i])
                x1 = min(1, xx[i] + 0.5 * w_[i])
                y0 = max(0, yy[i] - 0.5 * h_[i])
                y1 = min(1, yy[i] + 0.5 * h_[i])
                l_x.append((x1 + x0) / 2)
                l_y.append((y1 + y0) / 2)
                l_w.append(x1 - x0)
                l_h.append(y1 - y0)
            info = pd.DataFrame([l_x, l_y, l_w, l_h], index=["x", "y", "w", "h"]).T
            info = info.dropna()
            label.append(info)

            deg_region = [deg_top_left, deg_bot_right]
            train_deg_region.append(deg_region)

    return train_folder, train_deg_region, center_index, label
