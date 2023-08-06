"""Read files with data hidden inside them through Steganography
Supported files:
    wav

Functions:

    readAudio(audio_file: str, output_file: str, depth: int) -> (bytes) data

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

__all__ = ["readAudio"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

import wave
import array
from .RawReader import readRaw


def readAudio(audio_file: str, output_file: str, depth: int) -> bytes:
    """Read steganography data in a wav file

        Parameters:
            audio_file (str):  The path to the audio file to read
            output_file (str): The path to the file where the output data should be stored
            depth (int):       The bit depth to read

        Returns:
            byte_string (bytes): Hidden data
    """
    with wave.open(audio_file, 'rb') as out_wavefile:
        sizes = {1: 'B', 2: 'h', 4: 'i'}
        samp_size = out_wavefile.getsampwidth()
        frmt = sizes[samp_size]

        initial_data = array.array(frmt)
        initial_data.frombytes(out_wavefile.readframes(out_wavefile.getnframes()))

    byte_string = readRaw(initial_data, depth)

    try:
        with open(output_file, "wb") as f:
            f.write(byte_string)
    except TypeError:
        pass

    return byte_string
