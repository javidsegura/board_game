from PySide6.QtCore import QUrl, QTimer
from PySide6.QtMultimedia import QSoundEffect

import os

class SoundEffects():
    def __init__(self):
        self.cash_out_sound = QSoundEffect()
        self.cash_out_sound.setSource(QUrl.fromLocalFile("utils/sound_effects/cashier-quotka-chingquot-sound-effect-129698.wav"))
        self.cash_out_sound.setVolume(.5)
        self.cash_out_sound.setLoopCount(1)

    def play_cashout(self):
        if self.cash_out_sound.isLoaded():
            self.cash_out_sound.play()
            QTimer.singleShot(100, lambda: None)
        else:
            print("Sound effect not loaded properly")