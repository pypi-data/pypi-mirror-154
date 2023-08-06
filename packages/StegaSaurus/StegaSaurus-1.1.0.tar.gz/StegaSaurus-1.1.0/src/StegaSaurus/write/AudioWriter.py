"""Create files with data hidden inside them through Steganography
Supported files:
    wav

Functions:

    writeAudio(in_audio_file: str, out_audio_file: str, data_file: str, depth: int) -> (Audio) Image data as a list

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

__all__ = ["writeAudio"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

import wave
import array
from .RawWriter import writeRaw


def writeAudio(in_audio_file: str, out_audio_file: str, data_file: str, depth: int) -> list:
    """Write steganography data to almost any audio file

        Parameters:
            in_audio_file (str):  The path to the audio file to write
            out_audio_file (str): The path to the file where the output data should be stored
            data_file (str):      The path to the data file to hide
            depth (int):          The bit depth to write

        Returns:
            final_data (list): Audio data as a list
    """
    with wave.open(in_audio_file, 'rb') as wavefile:
        sizes = {1: 'B', 2: 'h', 4: 'i'}
        channels = wavefile.getnchannels()
        samp_size = wavefile.getsampwidth()
        frmt = sizes[samp_size]

        initial_data = array.array(frmt)
        initial_file_data = array.array('B')
        file_data_bits = array.array('B')
        initial_data.frombytes(wavefile.readframes(wavefile.getnframes()))

        with open(data_file, "rb") as f:
            file_data = f.read()
        initial_file_data.frombytes(file_data)
        for byte in initial_file_data:
            for bit in range(7, -1, -1):
                file_data_bits.append(byte >> bit & 1)
        for _ in range(len(initial_data) - len(file_data_bits)):
            file_data_bits.append(0)

        final_data = writeRaw(initial_data, file_data_bits, depth)

        with wave.open(out_audio_file, 'wb') as out_wavefile:
            out_wavefile.setnchannels(channels)
            out_wavefile.setsampwidth(samp_size)
            out_wavefile.setframerate(wavefile.getframerate())
            out_wavefile.setnframes(len(final_data))
            out_wavefile.setcomptype(wavefile.getcomptype(), wavefile.getcompname())
            out_wavefile.writeframesraw(final_data.tobytes())

    return final_data.tolist()


if __name__ == "__main__":
    location2 = "C:\\Users\\Alexander\\PycharmProjects\\StegaSaurus\\src\\"
    writeAudio(location2 + 'sine.wav', location2 + 'sine2.wav', location2 + "Untitled.jpg", 2)
