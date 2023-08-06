"""Create files with data hidden inside them through Steganography
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

    writeImage(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> (list) Image data as a list

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

__all__ = ["writeImageAdvanced"]
__author__ = "Alexander Bisland"
__version__ = "1.0.2"
supported_from = "3.8.1"

from .SimpleImageWriter import writeImageSimple

advanced = True
try:
    from .AdvancedImageWriter import writeImageAdvanced
except ModuleNotFoundError:
    advanced = False


def writeImage(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> list:
    """Write steganography data to almost any image file (If PIL is installed)

        Parameters:
            in_image_file (str):  The path to the image to write
            out_image_file (str): The path to the file where the output data should be stored
            data_file (str):      The path to the data file to hide
            depth (int):          The bit depth to write

        Returns:
            final_data (list): Image data as a list
    """
    if advanced:
        return writeImageAdvanced(in_image_file, out_image_file, data_file, depth)
    else:
        return writeImageSimple(in_image_file, out_image_file, data_file, depth)
