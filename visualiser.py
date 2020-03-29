import audioInput
import pygame
from time import time
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from random import randint
import customWidgets as cw


class Window:
    def __init__(self, audioDevice, screens: tuple = (), fpsLimiter=1):
        self.audioDevice = audioDevice

        self.fpsLimiter = fpsLimiter
        self.screens = screens
        self._running = True

        self.width, self.height = (len(self.screens) - 1) * 10, 0
        for i in self.screens:
            self.width += i.resolution.x
            self.height = max(self.height, i.resolution.y)
        self.size = self.width, self.height

        self.counter = 0
        self.fps = 0

    def init(self):
        pygame.init()
        pygame.display.set_caption("Visualizer v0.2b")
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._running = True

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def loop(self):
        t = time()
        self.audioDevice.getData()

        self.counter += 1

        if self.counter % self.fpsLimiter == 0:
            self.fps = 0
            try:
                self.fps = 1 / ((time() - t) * self.fpsLimiter)
            except ZeroDivisionError:
                pass
            except Exception as e:
                print(e)

            pygame.display.update()

    def render(self):
        self.screen.fill(black)

        tempX = 0
        for i in self.screens:
            display = i.render()
            for nx, x in enumerate(display):
                for ny, y in enumerate(x):
                    try:
                        pygame.draw.rect(self.screen, y,
                                     pygame.Rect(tempX + nx * (i.pixel.x + i.pxDist),
                                                 i.resolution.y + i.pxDist - (ny + 1) * (i.pixel.y + i.pxDist),
                                                 i.pixel.x,
                                                 i.pixel.y))
                    except Exception as e:
                        print(e)
                        print(y)
            tempX += i.resolution.x + 10

        self.screen.blit(pygame.font.SysFont('Arial Bold', 30).render('FPS: %5.2f' % self.fps, False, red), (10, 10))

    def cleanup(self):
        pygame.quit()

    def execute(self):
        if self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        else:
            self.cleanup()


class Dimension:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDiagonal(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def setDimension(self, s: tuple):
        self.x = s[0]
        self.y = s[1]


class Screen:
    def __init__(self, size: Dimension, pixel: Dimension, pxDist: int) -> None:

        self.updateSize(size, pixel, pxDist)
        self.settings = None

    def render(self):
        raise NotImplementedError()

    def updateSize(self, size: Dimension = None, pixel: Dimension = None, pxDist: int = None):
        if size is not None: self.size = size
        if pixel is not None: self.pixel = pixel
        if pxDist is not None: self.pxDist = pxDist
        self.resolution = Dimension(self.size.x * (self.pixel.x + self.pxDist) - self.pxDist,
                                    self.size.y * (self.pixel.y + self.pxDist) - self.pxDist)


class Spectrum(Screen):
    number = 0

    def __init__(self, audioDevice: audioInput.AudioInput, size: Dimension = Dimension(14, 20),
                 pixel: Dimension = Dimension(25, 10), pxDist: int = 5,
                 sens: float = 0.03, topDelay: int = 0):
        self.name = self.__class__.__name__ + ' - ' + str(Spectrum.number)
        Spectrum.number += 1

        self.audioDevice = audioDevice
        self.findex = [0, self.audioDevice.indexFromFreq(30), self.audioDevice.indexFromFreq(60),
                       self.audioDevice.indexFromFreq(90), self.audioDevice.indexFromFreq(120),
                       self.audioDevice.indexFromFreq(170),
                       self.audioDevice.indexFromFreq(220), self.audioDevice.indexFromFreq(410),
                       self.audioDevice.indexFromFreq(600), self.audioDevice.indexFromFreq(800),
                       self.audioDevice.indexFromFreq(1000),
                       self.audioDevice.indexFromFreq(1500), self.audioDevice.indexFromFreq(2000),
                       self.audioDevice.indexFromFreq(3750), self.audioDevice.indexFromFreq(4500)]

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

        # Create settings menu for display
        self.settings = self.Menu(self)

    class Menu(tk.Frame):
        def __init__(self, screen):
            self.screen = screen

        def create(self, *args, **kwargs):
            tk.Frame.__init__(self, width=200, height=100, *args, **kwargs)
            self.grid(column=0, row=0)

            tk.Label(self, text=self.screen.name).pack(fill=X, expand=True)

            # Colour Mode Settings
            cw.ColourModeSettings(self, self.screen).pack(fill=X)

            # Delay Settings
            cw.DelaySettings(self, self.screen).pack(fill=X)

            # Sensitivity Settings
            cw.SensitivitySettings(self, self.screen).pack(fill=X)

            # Beat Detection Sensitivity Settings
            cw.BeatSensitivitySettings(self, self.screen).pack(fill=X)

            # Beat Detection Bar Settings
            cw.BeatBarSettings(self, self.screen).pack()

            # Beat Detection Threshold Settings
            cw.BeatThresholdSettings(self, self.screen).pack(fill=X)

            # Colour Crossfade Sensitivity Settings
            cw.CrossfadeSpeedSettings(self, self.screen).pack(fill=X)

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
            if j > self.size.y*0.9:
                res.append(red)
            elif j > self.size.y*0.7:
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

    def __init__(self, audioDevice: audioInput.AudioInput, size: int = 40, pixel: Dimension = Dimension(15, 5), pxDist: int = 5,
                 sens: float = 0.03, topDelay: int = 0, align: int = 0):
        super().__init__(audioDevice, Dimension(1, size), pixel, pxDist, sens, topDelay)
        self.align = align      # Align 0:Left, 1:Right, 2:Center

        self.beatDetectionBar = 0

    def calcBars(self):
        self.findex.sort()
        self.bar = []
        self.bar.append(self.sens * self.audioDevice.getSpectralBar(self.findex[0], self.findex[1]))

    def addBand(self, f1=90, f2=120):
        self.findex = [self.audioDevice.indexFromFreq(f1), self.audioDevice.indexFromFreq(f2)]


class Application(tk.Tk):
    def __init__(self, window: Window, *args, **kwargs):
        # Initiating tkinter application
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Integrating pygame window
        self.window = window
        self.frame = tk.Frame(self, width=self.window.width, height=self.window.height)
        self.frame.grid(row=0, column=0, rowspan=10)
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Settings Panel
        settingSelector = tk.Frame(self)
        tk.Label(settingSelector, text="Settings for screen: ").pack(side=LEFT)
        self.settingsSelectorCombo = ttk.Combobox(settingSelector, values=[i.name for i in self.window.screens],
                                                  width=30)
        self.settingsSelectorCombo.bind("<<ComboboxSelected>>", self.selectSettingPanel)
        self.settingsSelectorCombo.current(0)
        self.settingsSelectorCombo.pack(side=LEFT)
        settingSelector.grid(row=0, column=1, sticky=NW)
        self.SettingsContainer = tk.Frame(self)
        self.SettingsContainer.grid(row=1, column=1, sticky=N)
        # Create all the Frames for the settings panels
        for n, i in enumerate(self.window.screens):
            i.settings.create(self.SettingsContainer)
        self.selectSettingPanel(None)

    def selectSettingPanel(self, event):
        self.window.screens[self.settingsSelectorCombo.current()].settings.tkraise()

    def open(self):
        self.window.init()
        while True:
            self.update()
            self.window.execute()

    def quit(self):
        self.window._running = False
        self.destroy()


purple = (128, 0, 128)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
cyan = (64, 224, 208)
black = (0, 0, 0)
white = (255, 255, 255)

if __name__ == "__main__":
    A = audioInput.AudioInput(4096, 96000, 4096, 1)
    app = Application(Window(A, screens=(Spectrum(A, topDelay=0), SpectrumLine(A, topDelay=0)), fpsLimiter=1))
    app.open()
