import PIL
from PIL import Image


def is_image(file: str) -> bool:
    """
    Checks if a file is an image.
    :param file: File to be checked.
    :return: If the file is an image.
    """
    try:
        image = Image.open(file)
        image.verify()  # closes the image
        return True
    except (PIL.UnidentifiedImageError, OSError):
        return False
