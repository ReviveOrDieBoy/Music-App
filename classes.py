import vlc
import mutagen
import os

class Song:
    def __init__(self, path):
        self.path = path
        self.length = mutagen.File(self.path).info.length
        self.track = vlc.MediaPlayer(self.path)
        self.name = os.path.basename(self.path)
        self.name = os.path.splitext(self.name)[0]

if __name__ == "main":
    path = None
