import tkinter
from .RawReader import readRaw

img = None
tk = tkinter.Tk()
tk.withdraw()


def readImageSimple(image_file: str, output_file: str, depth: int) -> bytes:
    global img, tk
    img = tkinter.PhotoImage(file=image_file, master=tk)
    tk.image = img
    pixels = []
    for index in range(img.width() * img.height()):
        pixels.append(img.get(index % img.width(), index // img.width()))
    pixels = [channel for pixel in pixels for channel in pixel]

    byte_string = readRaw(pixels, depth)

    try:
        with open(output_file, "wb") as f:
            f.write(byte_string)
    except TypeError:
        pass

    return byte_string
