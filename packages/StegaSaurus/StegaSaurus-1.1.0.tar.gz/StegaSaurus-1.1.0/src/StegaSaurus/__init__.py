"""Create and read files with data hidden inside them through Steganography
Supported files:
    Standard:
        wav
        png
        gif
    If you install PIL
        jpg
        bmp
        (most other image formats)

Functions:

    read.AudioReader.readAudio(audio_file: str, output_file: str, depth: int) -> (bytes) data
    read.ImageReader.readImage(image_file: str, output_file: str, depth: int) -> (bytes) data
    read.RawReader.readRaw(initial_data: Union[array.array, list], depth: int) -> (bytes) data
    write.AudioWriter.writeAudio(in_audio_file: str, out_audio_file: str, data_file: str, depth: int) ->
                                                                                            (list) Audio data as a list
    write.ImageWriter.writeImage(in_image_file: str, out_image_file: str, data_file: str, depth: int) ->
                                                                                            (list) Image data as a list
    write.RawWriter.writeRaw(initial_data: array.array, file_data_bits: Union[array.array, list], depth: int) ->
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

__all__ = ["AudioReader", "ImageReader", "RawReader", "AudioWriter", "ImageWriter", "RawWriter"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from .read import AudioReader, ImageReader, RawReader
from .write import AudioWriter, ImageWriter, RawWriter
