import cv2
import numpy as np


def sliding_window(image, path, stepSize, windowSize, height, width):
    """
    Cropped the image by using sliding window methods with no overlapping
    between the image. Then randomly locate the image in a 832*832 mask.

    Parameters
    ----------
    image: numpy.array
        image matrix
    stepSize: int
        the size of each sliding window step
    windowSize: tuple or array like
        the size of the sliding window (size of cropped image)
    height: int
        the vertical length of the original image in index
    width: int
        the horizontal length of the original image in index

    Returns
    -------
    x: int
        output the next x coordinate
    y: int
        output the next y coordinate
    """
    count = 0
    l = [] # noqa
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            mask = np.zeros([416, 416, 3], dtype="uint8")
            if (y + windowSize[1]) <= height and (x + windowSize[0]) <= width:
                slide = image[y: y + windowSize[1], x: x + windowSize[0], :]
                l.append(slide)
                cv2.imwrite(path + str(count) + ".png", slide)
                count = count + 1
            if (y + windowSize[1]) > height and (x + windowSize[0]) <= width:
                slide = image[y:height, x: x + windowSize[0], :]
                mask[0: height - y, :, :] = slide
                l.append(mask)
                cv2.imwrite(path + str(count) + ".png", mask)
                count = count + 1
            if (y + windowSize[1]) <= height and (x + windowSize[0]) > width:
                slide = image[y: y + windowSize[1], x:width, :]
                mask[:, 0: width - x, :] = slide
                l.append(mask)
                cv2.imwrite(path + str(count) + ".png", mask)
                count = count + 1
            if (y + windowSize[1]) > height and (x + windowSize[0]) > width:
                slide = image[y: y + windowSize[1], x:width, :]
                mask[0: height - y, 0: width - x, :] = slide
                l.append(mask)
                cv2.imwrite(path + str(count) + ".png", mask)
                count = count + 1
    return x, y
