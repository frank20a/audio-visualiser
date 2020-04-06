from random import randint
import tkinter as tk

from screen import Screen
import audioInput
from dimension import Dimension
import settingsPanels as sp
from colors import *


class Spectrum(Screen):
    number = 0

    def __init__(self, audioDevice: audioInput.AudioInput, size: Dimension = Dimension(14, 20),
                 pixel: Dimension = Dimension(25, 10), pxDist: int = 5,
                 sens: float = 0.03, topDelay: int = 0):
        self.name = self.__class__.__name__ + ' - ' + str(Spectrum.number)
        Spectrum.number += 1

        self.audioDevice = audioDevice
        self.findex = [0]
        freqs = [30, 60, 90, 120, 170, 220, 410, 600, 800, 1000, 1500, 2000, 3750, 4500]
        self.findex = self.findex + [self.audioDevice.indexFromFreq(f) for f in freqs]

        self.sens = sens
        self.topDelay = topDelay
        super().__init__(size, pixel, pxDist)
        self.addBand()
        self.calcBars()
        self.changePalette("gradientBeat")
        self.counter = 0

        # Colour Crossfade Variables
        self.crossfadeSpeed = 8
        self.r = 255
        self.g = 75
        self.b = 76

        # Beat Detection Variables
        self.beatDetectSensitivity = 2.2
        self.beatDetectThreshold = 12
        self.beatDetectionBar = 3
        self.beatDetect = [0 for i in range(20)]

    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.SpectrumMenu(parent, self)
        return self.settings

    def calcBars(self):
        self.findex.sort()
        self.bar = []
        for i in range(len(self.findex) - 1):
            self.bar.append(self.sens * self.audioDevice.getSpectralBar(self.findex[i], self.findex[i + 1]))

    def addBand(self, x=0):
        if x > 0: self.findex.append(self.audioDevice.indexFromFreq(x))
        self.tops = [[0, 0] for i in range((len(self.findex) - 1) * 2)]
        self.updateSize(size=Dimension(len(self.findex) - 1, self.size.y))

    def beatDetectColour(self):
        self.beatDetect.insert(0, self.bar[self.beatDetectionBar])
        self.beatDetect.pop()

        if self.beatDetect[0] > sum(self.beatDetect) / len(self.beatDetect) * self.beatDetectSensitivity and \
                self.beatDetect[0] > self.beatDetectThreshold:
            self.r = randint(0, 255)
            self.g = randint(0, 255)
            self.b = randint(0, 255)

        return [(min(max(self.r, 75), 240), min(max(self.g, 75), 240), min(max(self.b, 75), 240)) for i in
                range(self.size.y)]

    def beatDetectGradient(self):
        t = self.beatDetectColour()
        return self.gradient(t[0], (t[0][2], t[0][0], t[0][1]))

    def crossfadeColours(self):
        if self.counter % self.crossfadeSpeed == 0:
            if self.b <= 75 and self.g > 75:
                self.b = 75
                self.r += 20
                self.g -= 20
            if self.g <= 75 and self.r > 75:
                self.g = 75
                self.r -= 20
                self.b += 20
            if self.r <= 75 and self.b > 75:
                self.r = 75
                self.g += 20
                self.b -= 20
        return [(min(max(self.r, 75), 240), min(max(self.g, 75), 240), min(max(self.b, 75), 240)) for i in
                range(self.size.y)]

    def peakingColours(self):
        res = []
        for j in range(self.size.y):
            if j > self.size.y * 0.9:
                res.append(red)
            elif j > self.size.y * 0.7:
                res.append(yellow)
            else:
                res.append(green)
        return res

    def gradient(self, c1, c2):
        res = []
        for i in range(self.size.y):
            res.append((
                c1[0] + i * (c2[0] - c1[0]) / (self.size.y - 1),
                c1[1] + i * (c2[1] - c1[1]) / (self.size.y - 1),
                c1[2] + i * (c2[2] - c1[2]) / (self.size.y - 1)
            ))
        return res

    def gradientCrossfadeColours(self):
        return self.gradient(self.crossfadeColours()[0], (
            self.crossfadeColours()[0][1], self.crossfadeColours()[0][0], self.crossfadeColours()[0][2]))

    def changePalette(self, x, *args):
        class InvalidPaletteException(Exception):
            """Raise when given invalid palette argument"""

            def __init__(self):
                super(InvalidPaletteException, self).__init__("Invalid palette argument")

        # self.beatDetectColour
        # self.crossfadeColours
        # self.peakingColours()
        # self.gradient(green, red)
        # self.gradientCrossfadeColours
        # self.beatDetectGradient

        if x == "peaking":
            self.palette = self.peakingColours()
        elif x == "beat":
            self.palette = self.beatDetectColour
        elif x == "gradient":
            self.palette = self.gradient(args[0], args[1])
        elif x == "cross":
            self.r = 255
            self.g = 75
            self.b = 76
            self.palette = self.crossfadeColours
        elif x == "gradientCross":
            self.r = 255
            self.g = 75
            self.b = 76
            self.palette = self.gradientCrossfadeColours
        elif x == "gradientBeat":
            self.palette = self.beatDetectGradient
        else:
            raise InvalidPaletteException

    def render(self):
        self.calcBars()

        self.counter += 1
        if callable(self.palette):
            col = self.palette()
        else:
            col = self.palette

        res = []

        for n, i in enumerate(self.bar):
            t = [black for i in range(self.size.y)]

            for j in range(min(int(i) + 1, self.size.y)): t[j] = col[j]

            if self.topDelay > 0:
                if i > self.tops[n][0]:
                    self.tops[n][0] = min(int(i), self.size.y)
                    self.tops[n][1] = 0
                if self.tops[n][1] % self.topDelay == 0: self.tops[n][0] -= 1
                if self.tops[n][0] >= 0:
                    topos = min(self.tops[n][0] + 1, self.size.y - 1)
                    t[topos] = col[topos]
                    self.tops[n][1] += 1

            res.append(t)

        return res


class SpectrumLine(Spectrum):
    number = 0

    def __init__(self, audioDevice: audioInput.AudioInput, size: int = 40, pixel: Dimension = Dimension(15, 5),
                 pxDist: int = 5,
                 sens: float = 0.03, topDelay: int = 0, align: int = 0):
        super().__init__(audioDevice, Dimension(1, size), pixel, pxDist, sens, topDelay)
        self.align = align  # Align 0:Left, 1:Right, 2:Center

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
