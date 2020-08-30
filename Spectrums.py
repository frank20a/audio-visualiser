from random import randint
import tkinter as tk
from math import exp

from Screen import Screen
import AudioInput
from Dimension import Dimension
import SettingsPanels as sp
from Colors import *
from Exceptions import ConflictingSizes


class Spectrum(Screen):
    number = 0

    def __init__(self, audioDevice: AudioInput.AudioInput, size: Dimension = Dimension(31, 40), freqs: tuple = (),
                 pixel: Dimension = Dimension(17, 7), pxDist: int = 5, sens: float = 0.05, topDelay: int = 0):
        self.name = self.__class__.__name__ + ' - ' + str(Spectrum.number)
        Spectrum.number += 1

        # Audio setup
        self.audioDevice = audioDevice
        if not freqs:
            freqs = (20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
                     2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000)
        self.findex = [self.audioDevice.indexFromFreq(f) for f in freqs]
        # print(self.findex)

        # Screen attributes
        self.sens = sens
        self.topDelay = topDelay
        self.topFrameDrop = 1
        self.fillDelay = False
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
        self.beatDetectionBar = 6
        self.beatDetect = [0 for i in range(20)]

    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.SpectrumMenu(parent, self)
        return self.settings

    def changeSize(self, size) -> None:
        self.updateSize(size=size)

    def changePixel(self, size) -> None:
        self.updateSize(pixel=size)

    def changeDist(self, size) -> None:
        self.updateSize(pxDist=size)

    def calcBars(self) -> None:
        self.findex.sort()

        # ========= DEPRECATED =========
        # self.bar = []
        # for i in range(len(self.findex) - 1):
        #     self.bar.append(self.sens * self.audioDevice.getSpectralBar(self.findex[i], self.findex[i + 1]))
        # ==============================

        self.bar = [self.sens * self.audioDevice.getSpectralBar(i) for i in self.findex][:self.size.x]

    def addBand(self, x=0) -> None:
        if x > 0: self.findex.append(self.audioDevice.indexFromFreq(x))
        self.tops = [[0, 0] for i in range(len(self.findex))]
        self.updateSize(size=Dimension(len(self.findex), self.size.y))

    def beatDetectColour(self) -> list:
        try:
            self.beatDetect.insert(0, self.bar[self.beatDetectionBar])
        except IndexError:
            self.beatDetect.insert(0, self.bar[self.size.x - 1])
        self.beatDetect.pop()

        if self.beatDetect[0] > sum(self.beatDetect) / len(self.beatDetect) * self.beatDetectSensitivity and \
                self.beatDetect[0] > self.beatDetectThreshold:
            self.r = randint(0, 255)
            self.g = randint(0, 255)
            self.b = randint(0, 255)

        return [(min(max(self.r, 75), 255), min(max(self.g, 75), 255), min(max(self.b, 75), 255)) for i in
                range(self.barLength)]

    def beatDetectGradient(self) -> list:
        t = self.beatDetectColour()
        return self.exponential_gradient(t[0], (t[0][2], t[0][0], t[0][1]))

    def crossfadeColours(self) -> list:
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
                range(self.barLength)]

    def peakingColours(self) -> list:
        res = []
        for j in range(self.barLength):
            if j > self.barLength * 0.9:
                res.append(red)
            elif j > self.barLength * 0.7:
                res.append(yellow)
            else:
                res.append(green)
        return res

    def exponential_gradient(self, c1, c2, a: float = 2.0) -> list:
        res = []
        for i in range(self.barLength):
            res.append((
                int(c1[0] + (1-(exp(-a*i/(self.barLength - 1)))) * (c2[0] - c1[0])),
                int(c1[1] + (1-(exp(-a*i/(self.barLength - 1)))) * (c2[1] - c1[1])),
                int(c1[2] + (1-(exp(-a*i/(self.barLength - 1)))) * (c2[2] - c1[2]))
            ))
        return res

    def linear_gradient(self, c1, c2) -> list:
        res = []
        for i in range(self.barLength):
            res.append((
                int(c1[0] + i * (c2[0] - c1[0]) / (self.barLength - 1)),
                int(c1[1] + i * (c2[1] - c1[1]) / (self.barLength - 1)),
                int(c1[2] + i * (c2[2] - c1[2]) / (self.barLength - 1))
            ))
        return res

    def gradientCrossfadeColours(self) -> list:
        return self.exponential_gradient(self.crossfadeColours()[0], (
            self.crossfadeColours()[0][1], self.crossfadeColours()[0][0], self.crossfadeColours()[0][2]))

    def changePalette(self, x, *args) -> None:
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
            self.palette = self.exponential_gradient(args[0], args[1])
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

    def render(self) -> list:
        self.calcBars()

        self.counter += 1
        if callable(self.palette):
            col = self.palette()
        else:
            col = self.palette

        res = []

        for n, i in enumerate(self.bar):
            t = [black for i in range(self.barLength)]

            for j in range(min(int(i) + 1, self.barLength)): t[j] = col[j]

            if self.topDelay > 0:

                if i > self.tops[n][0]:
                    self.tops[n][0] = min(int(i), self.barLength)
                    self.tops[n][1] = 0
                if self.tops[n][1] % self.topDelay == 0: self.tops[n][0] -= self.topFrameDrop
                if self.tops[n][0] >= 0:
                    topos = min(self.tops[n][0] + 1, self.barLength - 1)
                    if self.fillDelay:
                        for j in range(min(topos, self.barLength)): t[j] = col[j]
                    else:
                        t[topos] = col[topos]
                    self.tops[n][1] += 1

            res.append(t)

        # if len(res) != self.size.x:raise ConflictingSizes("Number of bars and x-dimension are different")
        return res

    def cleanup(self):
        print("Closed", self.name)


class SpectrumBar(Spectrum):
    number = 0

    def __init__(self, audioDevice: AudioInput.AudioInput, freq: int = 100, size: int = 40,
                 pixel: Dimension = Dimension(17, 7), pxDist: int = 5, sens: float = 0.05, topDelay: int = 0,
                 align: int = 0):

        self.align = align  # Align 0:Bottom, 1:Top, 2:Center
        self.freq = freq

        super().__init__(audioDevice, size=Dimension(1, size), pixel=pixel, pxDist=pxDist, sens=sens,
                         topDelay=topDelay)

        self.beatDetectionBar = 0

    def createSettings(self, parent) -> tk.Frame:
        self.settings = sp.LineMenu(parent, self)
        return self.settings

    def render(self) -> list:

        res = Spectrum.render(self)
        if self.align == 1: res[0] = res[0][::-1]
        if self.align == 2:
            if self.size.y % 2 == 0:
                res[0] = res[0][-2::-2] + res[0][::2]
            else:
                res[0] = res[0][-2::-2] + [res[0][0]] + res[0][1::2]

        return res

    def addBand(self, freq: int = None) -> None:
        if freq is None: return

        self.freq = (freq)
        self.findex = [self.audioDevice.indexFromFreq(self.freq)]
        self.tops = [[0, 0]]

    def getFreq(self) -> int:
        return self.freq

    def changeSize(self, size) -> None:
        self.updateSize(size=Dimension(1, size))


class SpectrumLine(Spectrum):
    number = 0

    def __init__(self, audioDevice: AudioInput.AudioInput, size: int = 31, freqs: tuple = (),
                 pixel: Dimension = Dimension(10, 10), pxDist: int = 0, sens: float = 0.05, clipping=40):

        super().__init__(audioDevice, size=Dimension(size, 1), freqs=freqs, pixel=pixel, pxDist=pxDist, sens=sens)
        self.barLength = clipping
        # self.changePalette("gradient", (0, 184, 18), (224, 7, 7))
        self.changePalette("gradient", (255, 255, 0), (255, 0, 0))

    def render(self) -> list:
        self.calcBars()

        self.counter += 1
        if callable(self.palette):
            col = self.palette()
        else:
            col = self.palette

        res = []

        for i in self.bar:
            res.append([col[min(int(i), self.barLength-1)]])

        # if len(res) != self.size.x:raise ConflictingSizes("Number of bars and x-dimension are different")
        return res
