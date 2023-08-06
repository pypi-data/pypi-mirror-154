"""Create files with data hidden inside them through Steganography
Supported files:
    png
    gif

Functions:

    writeImageSimple(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> (list) Image data as a list

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

__all__ = ["writeImageSimple"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from .RawWriter import writeRaw
import array
import tkinter

img = None
tk = tkinter.Tk()
tk.withdraw()


def writeImageSimple(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> list:
    """Write steganography data to png and gif images

        Parameters:
            in_image_file (str):  The path to the image to write
            out_image_file (str): The path to the file where the output data should be stored
            data_file (str):      The path to the data file to hide
            depth (int):          The bit depth to read

        Returns:
            final_data (list): Image data as a list
    """
    global img, tk
    img = tkinter.PhotoImage(file=in_image_file, master=tk)
    tk.image = img
    pixels = []
    for index in range(img.width() * img.height()):
        pixels.append(img.get(index % img.width(), index // img.width()))
    pixels = [channel for pixel in pixels for channel in pixel]

    initial_data = array.array('B')
    initial_file_data = array.array('B')
    file_data_bits = array.array('B')
    initial_data.fromlist(pixels)

    with open(data_file, "rb") as f:
        file_data = f.read()
    initial_file_data.frombytes(file_data)
    for byte in initial_file_data:
        for bit in range(7, -1, -1):
            file_data_bits.append(byte >> bit & 1)
    for _ in range(len(initial_data) - len(file_data_bits)):
        file_data_bits.append(0)

    final_data = writeRaw(initial_data, file_data_bits, depth)

    position = 0
    for row in range(img.height()):
        for col in range(img.width()):
            colour = "{#%02x%02x%02x}" % (final_data[position], final_data[position + 1], final_data[position + 2])
            img.put(colour, (col, row))
            position += 3
    img.write(out_image_file, format=out_image_file[-3:])

    return final_data.tolist()
