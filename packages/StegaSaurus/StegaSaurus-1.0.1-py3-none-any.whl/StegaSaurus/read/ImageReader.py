from .SimpleImageReader import readImageSimple

advanced = True
try:
    from .AdvancedImageReader import readImageAdvanced
except ModuleNotFoundError:
    advanced = False


def readImage(image_file: str, output_file: str, depth: int) -> bytes:
    if advanced:
        return readImageAdvanced(image_file, output_file, depth)
    else:
        return readImageSimple(image_file, output_file, depth)
