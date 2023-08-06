import wave
import array
from .RawReader import readRaw


def readAudio(audio_file: str, output_file: str, depth: int) -> bytes:
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


if __name__ == "__main__":
    location2 = "C:\\Users\\Alexander\\PycharmProjects\\StegaSaurus\\src\\"
    readAudio(location2 + 'sine2.wav', location2 + "Untitled2.jpg", 2)
