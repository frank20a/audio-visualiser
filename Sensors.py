import tkinter as tk

import AudioInput
from Dimension import Dimension
import SettingsPanels as sp
from Spectrums import SpectrumLine
from math import exp, sin, pi


class BeatDetector(SpectrumLine):
    number = 0

    def __init__(self, audioDevice: AudioInput.AudioInput, freq: int = 80,
                 pixel: int = 120, pxDist: int = 0, delay=3):
        SpectrumLine.__init__(self, audioDevice, size=1, pixel=Dimension(pixel, pixel),
                              pxDist=pxDist, sens=0.05, freq=freq)

        self.beatDetectThreshold = 6
        self.delay = delay
        self.c = 0

    def createSettings(self, parent) -> tk.Frame:
        raise NotImplementedError

    def render(self):
        self.calcBars()

        try:
            self.beatDetect.insert(0, self.bar[0])
        except IndexError:
            self.beatDetect.insert(0, self.bar[self.size.x - 1])
        self.beatDetect.pop()

        if self.beatDetect[0] > sum(self.beatDetect) / len(self.beatDetect) * self.beatDetectSensitivity and \
                self.beatDetect[0] > self.beatDetectThreshold and self.c >= self.delay:
            self.c = 0
            self.resolveBeat()
            return [[(255, 255, 0)]]

        self.c += 1
        return [[(0, 0, 0)]]

    def resolveBeat(self):
        raise NotImplementedError


class BeatDetectorTCP(BeatDetector):
    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.BeatDetectorTCPMenu(parent, self)
        return self.settings

    def resolveBeat(self):
        pass