"""Create files with data hidden inside them through Steganography

Functions:

    writeRaw(initial_data: array.array, file_data_bits: Union[array.array, list], depth: int) ->
                                                                                             (array.array) Raw byte data

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

__all__ = ["writeRaw"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

import math
import array
from typing import Union


def writeRaw(initial_data: array.array, file_data_bits: Union[array.array, list], depth: int) -> array.array:
    """Write steganography data in raw byte data

        Parameters:
            initial_data (array.array):                The array of data to overwrite
            file_data_bits (Union[array.array, list]): The array to overwrite with
            depth (int):                               The bit depth to write

        Returns:
            final_data (array.array): Raw byte data as an array.array
    """
    final_data = array.array(initial_data.typecode)
    bit_depth = int(math.log2(depth))
    dec_remainder = 2 ** bit_depth

    for index in range(0, len(initial_data)):
        addition = ""
        for bit in file_data_bits[index * bit_depth:(index + 1) * bit_depth]:
            addition += str(bit)
        if addition == "":
            addition = "0"
        final_data.append(initial_data[index] // dec_remainder * dec_remainder + int(addition, 2))
    return final_data
