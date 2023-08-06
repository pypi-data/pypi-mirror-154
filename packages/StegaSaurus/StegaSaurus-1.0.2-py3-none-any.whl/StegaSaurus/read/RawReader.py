import array
import math
from typing import Union


def readRaw(initial_data: Union[array.array, list], depth: int) -> bytes:
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
