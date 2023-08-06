"""Read files with data hidden inside them through Steganography
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

    AudioReader.readAudio(audio_file: str, output_file: str, depth: int) -> (bytes) data
    ImageReader.readImage(image_file: str, output_file: str, depth: int) -> (bytes) data
    AdvancedImageReader.readImageAdvanced(image_file: str, output_file: str, depth: int) -> (bytes) data
    SimpleImageReader.readImageSimple(image_file: str, output_file: str, depth: int) -> (bytes) data
    RawReader.readRaw(initial_data: Union[array.array, list], depth: int) -> (bytes) data

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

__all__ = ["AudioReader", "ImageReader", "RawReader", "AdvancedImageReader", "SimpleImageReader"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from StegaSaurus.read import ImageReader
from StegaSaurus.read import AdvancedImageReader
from StegaSaurus.read import SimpleImageReader
from StegaSaurus.read import AudioReader
from StegaSaurus.read import RawReader
