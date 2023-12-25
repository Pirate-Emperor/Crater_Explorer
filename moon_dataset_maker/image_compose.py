from PIL import Image


def image_compose(
    image_size=3000,
    image_row=4,
    image_column=5,
    image_save_path="final.jpg",
    image_format=".png",
    width=13645,
    height=9097,
):
    """
    Combine several images into one large image.

    Parameters:
    ----------

    image_size: float
        size of the image pieces
    image_row: float
        image row spacing, number of rows combined into one image
    image_column: float
        image column spacing,  number of rows combined into one image
    image_save_path: string
        path to save the image
    image_format: string
        format of the image (.jpg, .png, .tif) to be saved

    Returns
    -------
    image in .jpg or .png or .tif format

    """
    final_image = Image.new("RGB", (width, height))
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):
            from_image = Image.open(
                "predict_B/" + str(image_column * (y - 1) + x - 1) + image_format
            )
            final_image.paste(from_image, ((x - 1) * image_size, (y - 1) * image_size))
    return final_image.save(image_save_path)
