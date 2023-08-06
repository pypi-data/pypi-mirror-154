"""Read files with data hidden inside them through Steganography
Supported files:
    Standard:
        png
        gif
    If you install PIL:
        jpg
        bmp
        (most other image formats)

Functions:

    readImage(image_file: str, output_file: str, depth: int) -> (bytes) data

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

__all__ = ["readImage"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from .SimpleImageReader import readImageSimple

advanced = True
try:
    from .AdvancedImageReader import readImageAdvanced
except ModuleNotFoundError:
    advanced = False


def readImage(image_file: str, output_file: str, depth: int) -> bytes:
    """Read steganography data in almost any image file (If PIL is installed)

        Parameters:
            image_file (str):  The path to the image to read
            output_file (str): The path to the file where the output data should be stored
            depth (int):       The bit depth to read

        Returns:
            byte_string (bytes): Hidden data
    """
    if advanced:
        return readImageAdvanced(image_file, output_file, depth)
    else:
        return readImageSimple(image_file, output_file, depth)
