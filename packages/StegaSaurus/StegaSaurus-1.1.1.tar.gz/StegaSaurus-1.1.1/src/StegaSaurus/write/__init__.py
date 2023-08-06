"""Create and read files with data hidden inside them through Steganography
Supported files:
    Standard:
        wav
        png
        gif
    If you install PIL:
        jpg
        bmp
        (most other image formats)

Functions:

    AudioWriter.writeAudio(in_audio_file: str, out_audio_file: str, data_file: str, depth: int) ->
                                                                                            (list) Audio data as a list
    ImageWriter.writeImage(in_image_file: str, out_image_file: str, data_file: str, depth: int) ->
                                                                                            (list) Image data as a list
    AdvancedImageWriter.writeImageAdvanced(in_image_file: str, out_image_file: str, data_file: str, depth: int) ->
                                                                                            (list) Image data as a list
    SimpleImageWriter.writeImageSimple(in_image_file: str, out_image_file: str, data_file: str, depth: int) ->
                                                                                            (list) Image data as a list
    RawWriter.writeRaw(initial_data: array.array, file_data_bits: Union[array.array, list], depth: int) ->
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

__all__ = ["AudioWriter", "ImageWriter", "RawWriter", "AdvancedImageWriter", "SimpleImageWriter"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from StegaSaurus.write import ImageWriter
from StegaSaurus.write import AdvancedImageWriter
from StegaSaurus.write import SimpleImageWriter
from StegaSaurus.write import AudioWriter
from StegaSaurus.write import RawWriter
