"""Read files with data hidden inside them through Steganography
Supported files:
    png
    gif
    jpg
    bmp
    (most other image formats)

Functions:

    readImageAdvanced(image_file: str, output_file: str, depth: int) -> (bytes) data

Misc variables:

    __all__
    __author__
    __version__
    supported_from

Other Info:
    Steganography is the technique of hiding secret data within an ordinary, non-secret, file or message in order to
    avoid detection; the secret data is then extracted at its destination. The use of steganography can be combined with
    encryption as an extra step for hiding or protecting data.
"""

__all__ = ["readImageAdvanced"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from .RawReader import readRaw
try:
    from PIL import Image
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install PIL with pip install PIL or use SimpleImageReader for non-jpeg images")


def readImageAdvanced(image_file: str, output_file: str, depth: int) -> bytes:
    """Read steganography data in almost any image file

        Parameters:
            image_file (str):  The path to the image to read
            output_file (str): The path to the file where the output data should be stored
            depth (int):       The bit depth to read

        Returns:
            byte_string (bytes): Hidden data
    """
    im = Image.open(image_file)
    im = im.convert("RGB")
    pixels = list(im.getdata())
    pixels = [channel for pixel in pixels for channel in pixel]

    byte_string = readRaw(pixels, depth)

    try:
        with open(output_file, "wb") as f:
            f.write(byte_string)
    except TypeError:
        pass

    return byte_string
