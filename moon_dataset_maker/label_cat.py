import numpy as np
import pandas as pd


def csv_txt(csv, txt):
    """
    transfer csv into txt format

    Parameters
    ----------
    csv: csv file or dataframe
        csv file to be converted
    txt: string

    Returns
    ----------
    txt file
    """
    with open(txt, "w") as f:
        for line in csv.values:
            f.write(
                str(int(line[0]))
                + " "
                + str(line[1])
                + " "
                + str(line[2])
                + " "
                + str(line[3])
                + " "
                + str(line[4])
                + "\n"
            )


def label_cat(path, path_to_save, i, j, dim_x, dim_y, size_x, size_y):
    """
    Stitch labels from small pictures into the whole image. Create a txt file
    with the crater location infomation.

    Parameters
    ----------
    path: string
        path of labels
    path_to_save: string
        path to save stiched labels
    i: int
        number of lines
    j: int
        number of columns
    dim_x: int
        x dimension of small image
    dim_y: int
        y dimension of small image
    size_x: int
        x dimension of whole image
    size_y: int
        y dimension of whole image

    Returns
    --------

    None
    """

    l = []  # noqa
    count = 0
    for m in range(i):
        for n in range(j):
            path_label = path + str(count + 1) + ".txt"
            txt = np.loadtxt(path_label)
            label = pd.DataFrame(txt)
            label.columns = [["c", "x", "y", "w", "h"]]
            label["x"] = (label["x"] * dim_x + n * dim_x) / size_x
            label["y"] = (label["y"] * dim_y + m * dim_y) / size_y
            label["w"] = (label["w"] * dim_x) / size_x
            label["h"] = (label["h"] * dim_y) / size_y
            l.append(label)
            count += 1
    df1 = l[0]
    for i in range(1, len(l)):
        df1 = df1.append(l[i])
    csv_txt(df1, path_to_save)
