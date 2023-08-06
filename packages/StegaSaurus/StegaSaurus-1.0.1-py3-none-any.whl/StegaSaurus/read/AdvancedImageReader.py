from .RawReader import readRaw
try:
    from PIL import Image
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install PIL with pip install PIL or use SimpleImageReader for non-jpeg images")


def readImageAdvanced(image_file: str, output_file: str, depth: int) -> bytes:
    im = Image.open(image_file)
    im = im.convert("RGB")
    pixels = list(im.getdata())
    pixels = [channel for pixel in pixels for channel in pixel]

    byte_string = readRaw(pixels, depth)

    try:
        with open(output_file, "wb") as f:
            f.write(byte_string)
    except TypeError:
        pass

    return byte_string
