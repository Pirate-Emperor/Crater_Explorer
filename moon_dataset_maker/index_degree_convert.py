def index_degree_convert(index, height, width, name="B"):
    """
    Convert index into latitude and longitude according to relative location
    on map.

    Parameters
    ----------
    index: list
        index list
    height: int
        number of lines of the whole picture array
    width: int
        number of columns of the whole picture array
    name: str
        name of picture, choose from 'A','B','C','D'

    Returns
    ----------
    degree: numpy.array or lists of list
        the corresponding latitude and longitude of the location

    Examples
    --------
    >>> index_degree_convert([1000, 1000], 13646, 27291, name="B")
    [41.70233035321706, -176.70220951962185]

    """
    i = index[0]
    j = index[1]

    if name == "B":
        new_i = 45 - (i / height) * 45
        new_j = -180 + (j / width) * 90
        degree = [new_i, new_j]
        return degree

    if name == "D":
        new_i = 45 - (i / height) * 45
        new_j = -90 + (j / width) * 90
        degree = [new_i, new_j]
        return degree

    if name == "A":
        new_i = 0 - (i / height) * 45
        new_j = -180 + (j / width) * 90
        degree = [new_i, new_j]
        return degree

    if name == "C":
        new_i = 0 - (i / height) * 45
        new_j = -90 + (j / width) * 90
        degree = [new_i, new_j]
        return degree
