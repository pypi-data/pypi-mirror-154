"""Read files with data hidden inside them through Steganography

Functions:

    readRaw(initial_data: Union[array.array, list], depth: int) -> (bytes) data

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

__all__ = ["readRaw"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

import array
import math
from typing import Union


def readRaw(initial_data: Union[array.array, list], depth: int) -> bytes:
    """Read steganography data in raw byte data

        Parameters:
            initial_data (Union[array.array, list]): The path to the image to read
            depth (int):                             The bit depth to read

        Returns:
            byte_string (bytes): Hidden data
    """
    bit_file_data = []
    byteslist = []

    bit_depth = int(math.log2(depth))
    dec_remainder = 2 ** bit_depth

    for index in range(0, len(initial_data)):
        data = format(initial_data[index] % dec_remainder, "b")
        data = "0" * (bit_depth - len(data)) + data
        for bit in data:
            bit_file_data.append(int(bit))
    for index in range(0, len(bit_file_data), 8):
        byte = ""
        for bit in bit_file_data[index:index+8]:
            byte += str(bit)
        byteslist.append(int(byte, 2))
    return bytes(byteslist)
