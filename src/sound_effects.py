from PySide6.QtCore import QUrl, QTimer
from PySide6.QtMultimedia import QSoundEffect

import os

class SoundEffects():
    def __init__(self):
        self.sounds = {
            'click': self.load_sound("utils/sound_effects/click.wav"),
            'win': self.load_sound("utils/sound_effects/win.wav"),
            'lose': self.load_sound("utils/sound_effects/error.wav"),
            # Add more sound effects here
        }

    def load_sound(self, file_path):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(file_path))
        sound.setVolume(1)
        sound.setLoopCount(1)
        return sound

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if sound.isLoaded():
                sound.play()
                QTimer.singleShot(100, lambda: None)
            else:
                print(f"Sound effect '{sound_name}' not loaded properly")
        else:
            print(f"Sound effect '{sound_name}' not found")

    # Convenience methods for specific sounds
    def play_click(self):
        self.play_sound('click')

    def play_win(self):
        self.play_sound('win')

    def play_lose(self):
        self.play_sound('lose')