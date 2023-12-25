import cv2


def picture_generate(folder, path_img, path_label, label, folder_name, photo):
    """
    Generate images and labels into the corresponding path provided.

    Parameters
    ----------
    folder: array
        array of the image data
    path_img: string
        path to store image files
    path_label: string
        path to save label files
    label: list
        list of labels
    folder_name: string
        name of folder, 'train' or 'val' or 'test'
    photo: string
        name of photo, choose from 'lunar_A','lunar_B','lunar_C','lunar_D'

    Returns
    --------

    None
    """

    if folder_name == "train":
        for i in range(len(folder)):
            cv2.imwrite(
                path_img + photo + "_" + str(i + 1) + ".jpg",
                cv2.cvtColor(folder[i], cv2.COLOR_RGB2BGR),
            )
            label[i].to_csv(
                path_label + photo + "_" + str(i + 1) + ".csv", header=None,
                index=None
            )
    if folder_name == "val":
        for i in range(len(folder)):
            cv2.imwrite(
                path_img + photo + "_" + str(i + 1) + ".jpg",
                cv2.cvtColor(folder[i], cv2.COLOR_RGB2BGR),
            )
            label[i].to_csv(
                path_label + photo + "_" + str(i + 1) + ".csv", header=None,
                index=None
            )
    if folder_name == "test":
        for i in range(len(folder)):
            cv2.imwrite(
                path_img + photo + "_" + str(i + 1) + ".jpg",
                cv2.cvtColor(folder[i], cv2.COLOR_RGB2BGR),
            )
            label[i].to_csv(path_label + str(i + 1) + ".csv", header=None,
                            index=None)
    print("Done.")
