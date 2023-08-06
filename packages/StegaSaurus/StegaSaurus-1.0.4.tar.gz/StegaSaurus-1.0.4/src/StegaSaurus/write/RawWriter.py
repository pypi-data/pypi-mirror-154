import math
import array
from typing import Union


def writeRaw(initial_data: array.array, file_data_bits: Union[array.array, list], depth: int) -> array.array:
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
