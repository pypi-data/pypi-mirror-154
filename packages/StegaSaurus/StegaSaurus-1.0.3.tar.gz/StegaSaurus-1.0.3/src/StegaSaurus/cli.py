from .read import AudioReader, ImageReader
from .write import AudioWriter, ImageWriter


def cli():
    location2 = "C:\\Users\\Alexander\\PycharmProjects\\StegaSaurus\\src\\"
    AudioWriter.writeAudio(location2 + 'sine.wav', location2 + 'sine2.wav', location2 + "untitled (2).jpg", 2)
    AudioReader.readAudio(location2 + 'sine2.wav', location2 + "Untitled2.jpg", 2)
    ImageWriter.writeImage(location2 + "mario.gif", location2 + "out.png", location2 + "Untitled2.jpg", 4)
    ImageReader.readImage(location2 + "out.png", location2 + "Untitled3.jpg", 4)
