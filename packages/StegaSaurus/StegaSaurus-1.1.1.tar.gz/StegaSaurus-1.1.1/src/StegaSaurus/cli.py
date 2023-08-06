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

    cli() -> (None)

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

__all__ = ["cli"]
__author__ = "Alexander Bisland"
__version__ = "1.1.2"
supported_from = "3.8.1"

from StegaSaurus.read import AudioReader, ImageReader
from StegaSaurus.write import AudioWriter, ImageWriter
import argparse
import os


def cli() -> None:
    """Create and read files with data hidden inside them through Steganography

        Parameters:
            (None)

        Returns:
            Nothing (None): Null
    """
    parser = argparse.ArgumentParser(description='(Optionally) Dependency-free library for steganography')
    parser.add_argument('input', type=argparse.FileType('r'), help='Input file path')
    parser.add_argument('--read', '-r', dest='option', action='store_const',
                        const="r", default="w", help='Decrypt Seganography file')
    parser.add_argument('--write', '-w', dest='option', action='store_const',
                        const="w", help='Encrypt Seganography file')
    parser.add_argument('--audio', '-a', dest='type', action='store_const',
                        const="a", default="i", help='Perform operation on audio file')
    parser.add_argument('--image', '-i', dest='type', action='store_const',
                        const="i", help='Perform operation on image file')
    parser.add_argument('--no-output', dest='no_output', action='store_const',
                        const=True, default=False, help='No output file for decryption')
    parser.add_argument('--output', type=argparse.FileType('w'), default=None, help='Output file path')
    parser.add_argument('--data', type=argparse.FileType('r'), default=None, help='Data file path (write only)')
    parser.add_argument('--depth', '-d', type=int, default=2, help='Bit depth (default is 2)')
    parser.add_argument('--raw', type=str, default=None, help='Raw data for if data file is not used')

    args = parser.parse_args()

    data = os.path.abspath(args.data.name)
    if args.raw is not None:
        data = args.raw
    if args.no_output:
        output_file = None
    else:
        output_file = os.path.abspath(args.output.name)
    if args.option == "w":
        if args.output is None:
            print("Output file is required")
            exit()
        if data is None:
            print("Data file is required")
            exit()
        if args.type == "a":
            AudioWriter.writeAudio(os.path.abspath(args.input.name), os.path.abspath(args.output.name), data,
                                   args.depth)
        else:
            ImageWriter.writeImage(os.path.abspath(args.input.name), os.path.abspath(args.output.name), data,
                                   args.depth)
    else:
        if args.output is None:
            print("Output file is required")
            exit()
        if args.type == "a":
            resp = AudioReader.readAudio(os.path.abspath(args.input.name), output_file, args.depth)
            if output_file is None:
                print(resp)
        else:
            resp = ImageReader.readImage(os.path.abspath(args.input.name), output_file, args.depth)
            if output_file is None:
                print(resp)


if __name__ == "__main__":
    cli()
