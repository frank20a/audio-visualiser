import tkinter as tk

import audioInput
from dimension import Dimension
import settingsPanels as sp
from spectrum import Spectrum
from math import exp, sin, pi


class ResponsiveBox(Spectrum):
    number = 0

    def __init__(self, audioDevice: audioInput.AudioInput, freqRange: tuple = (90, 120), size: int = 10,
                 pixel: int = 10, pxDist: int = 0, sens: float = 0.03, topDelay: int = 0):
        self.freqRage = freqRange

        Spectrum.__init__(self, audioDevice, Dimension(2 * size - 1, 2 * size - 1), Dimension(pixel, pixel), pxDist,
                          sens, topDelay)

        self.barLength = size
        self.beatDetectionBar = 0

    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.LineMenu(parent, self)
        return self.settings

    def render(self):
        size = int((self.size.x + 1) / 2)
        temp = Spectrum.render(self)[0]
        res = [[(0, 0, 0) for i in range(2 * size - 1)] for j in range(2 * size - 1)]

        size -= 1
        for n, i in enumerate(temp):
            for j in range(-n, n + 1):
                res[size - n][size + j] = i
                res[size + n][size + j] = i
                res[size + j][size - n] = i
                res[size + j][size + n] = i

        return res

    def addBand(self, freqRange=None):
        self.tops = [[0, 0] for i in range((len(self.findex) - 1) * 2)]
        if freqRange: self.freqRage = freqRange
        self.findex = [self.audioDevice.indexFromFreq(self.freqRage[0]),
                       self.audioDevice.indexFromFreq(self.freqRage[1])]

    def getFreqRange(self) -> tuple:
        return self.freqRage


class ResponsiveStar(ResponsiveBox):
    def render(self):
        size = int((self.size.x + 1) / 2)
        temp = Spectrum.render(self)[0]
        res = [[(0, 0, 0) for i in range(2 * size - 1)] for j in range(2 * size - 1)]

        size -= 1
        for n, i in enumerate(temp):
            res[size - n][size] = i
            res[size + n][size] = i
            res[size][size - n] = i
            res[size][size + n] = i
            res[size - n][size + n] = i
            res[size - n][size - n] = i
            res[size + n][size + n] = i
            res[size + n][size - n] = i

        return res


class ResponsiveHelix(ResponsiveBox):
    def render(self):
        size = int((self.size.x + 1) / 2)
        temp = Spectrum.render(self)[0]
        res = [[(0, 0, 0) for i in range(2 * size - 1)] for j in range(2 * size - 1)]

        size -= 1
        pr = 0
        for n, i in enumerate(temp):
            # int(n * exp((n - size) / size))
            for j in range(pr, max(pr + 1, int(n * sin(pi * n / size)))):
                res[size - n][size + j] = i
                res[size - n][size - n + j] = i
                res[size + n][size - j] = i
                res[size + n][size + n - j] = i
                res[size - j][size - n] = i
                res[size - j + n][size - n] = i
                res[size + j][size + n] = i
                res[size + j - n][size + n] = i
            pr = int(n * sin(pi * n / size))

        return res
