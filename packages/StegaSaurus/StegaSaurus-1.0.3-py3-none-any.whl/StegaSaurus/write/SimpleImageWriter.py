from .RawWriter import writeRaw
import array
import tkinter

img = None
tk = tkinter.Tk()
tk.withdraw()


def writeImageSimple(in_image_file: str, out_image_file: str, data_file: str, depth: int) -> list:
    global img, tk
    img = tkinter.PhotoImage(file=in_image_file, master=tk)
    tk.image = img
    pixels = []
    for index in range(img.width() * img.height()):
        pixels.append(img.get(index % img.width(), index // img.width()))
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
    for row in range(img.height()):
        for col in range(img.width()):
            colour = "{#%02x%02x%02x}" % (final_data[position], final_data[position + 1], final_data[position + 2])
            img.put(colour, (col, row))
            position += 3
    img.write(out_image_file, format=out_image_file[-3:])

    return final_data.tolist()
