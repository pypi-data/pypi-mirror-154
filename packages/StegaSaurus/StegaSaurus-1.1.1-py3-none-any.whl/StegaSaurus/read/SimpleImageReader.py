"""Read files with data hidden inside them through Steganography
Supported files:
    png
    gif

Functions:

    readImageSimple(image_file: str, output_file: str, depth: int) -> (bytes) data

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

__all__ = ["readImageSimple"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

import tkinter
from .RawReader import readRaw

img = None
tk = tkinter.Tk()
tk.withdraw()


def readImageSimple(image_file: str, output_file: str, depth: int) -> bytes:
    """Read steganography data in png and gif images

        Parameters:
            image_file (str):  The path to the image to read
            output_file (str): The path to the file where the output data should be stored
            depth (int):       The bit depth to read

        Returns:
            byte_string (bytes): Hidden data
    """
    global img, tk
    img = tkinter.PhotoImage(file=image_file, master=tk)
    tk.image = img
    pixels = []
    for index in range(img.width() * img.height()):
        pixels.append(img.get(index % img.width(), index // img.width()))
    pixels = [channel for pixel in pixels for channel in pixel]

    byte_string = readRaw(pixels, depth)

    try:
        with open(output_file, "wb") as f:
            f.write(byte_string)
    except TypeError:
        pass

    return byte_string
