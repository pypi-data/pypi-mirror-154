from .SimpleImageWriter import writeImageSimple

advanced = True
try:
    from .AdvancedImageWriter import writeImageAdvanced
except ModuleNotFoundError:
    advanced = False


def writeImage(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> list:
    if advanced:
        return writeImageAdvanced(in_image_file, out_image_file, data_file, depth)
    else:
        return writeImageSimple(in_image_file, out_image_file, data_file, depth)
