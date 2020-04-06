import tkinter as tk

import audioInput
from dimension import Dimension
import settingsPanels as sp
from spectrum import Spectrum


class ResponsiveBox(Spectrum):
    number = 0

    def __init__(self, audioDevice: audioInput.AudioInput, size: int = 10, pixel: int = 10,
                 pxDist: int = 5, sens: float = 0.03, topDelay: int = 0):
        super().__init__(audioDevice, Dimension(2 * size - 1, 2 * size - 1), Dimension(pixel, pixel), pxDist, sens,
                         topDelay)

        self.beatDetectionBar = 0

    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.LineMenu(parent, self)
        return self.settings

    def calcBars(self):
        self.findex.sort()
        self.bar = []
        self.bar.append(self.sens * self.audioDevice.getSpectralBar(self.findex[0], self.findex[1]))

    def addBand(self, f1=90, f2=120):
        self.findex = [self.audioDevice.indexFromFreq(f1), self.audioDevice.indexFromFreq(f2)]
