from .RawWriter import writeRaw
import array
try:
    from PIL import Image
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install PIL with pip install PIL or use SimpleImageReader for non-jpeg images")


def writeImageAdvanced(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> list:
    img = Image.open(in_image_file)
    img = img.convert("RGB")
    pixels = list(img.getdata())
    pixels = [channel for pixel in pixels for channel in pixel]

    initial_data = array.array('B')
    initial_file_data = array.array('B')
    file_data_bits = array.array('B')
    initial_data.fromlist(pixels)

    with open(data_file, "rb") as f:
        file_data = f.read()
    initial_file_data.frombytes(file_data)
    for byte in initial_file_data:
        for bit in range(7, -1, -1):
            file_data_bits.append(byte >> bit & 1)
    for _ in range(len(initial_data) - len(file_data_bits)):
        file_data_bits.append(0)

    final_data = writeRaw(initial_data, file_data_bits, depth)

    position = 0
    newimg = Image.new('RGB', (img.width, img.height), "black")
    for row in range(img.height):
        for col in range(img.width):
            newimg.putpixel((col, row), (final_data[position], final_data[position + 1], final_data[position + 2]))
            position += 3
    newimg.save(out_image_file)

    return final_data.tolist()
