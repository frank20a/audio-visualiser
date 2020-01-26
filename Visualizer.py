import AudioInput
import pygame
from random import randint
from time import time
from pygame.locals import *


class Dimension:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDiagonal(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def setDimension(self, s: tuple):
        self.x = s[0]
        self.y = s[1]


class Window:
    def __init__(self, screens: tuple = (), fpsLimiter=1):
        self.fpsLimiter = fpsLimiter
        self.screens = screens
        self._running = True
        # self.screen = None
        self.size = self.weight, self.height = 620, 600
        self.counter = 0
        self.fps = 0

    def init(self):
        pygame.init()
        pygame.display.set_caption("Visualizer v0.1a")
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._running = True

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def loop(self):
        t = time()
        A.getData()

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
        self.screen.blit(pygame.font.SysFont('Arial Bold', 30).render('FPS: %5.2f' % self.fps, False, red), (10, 10))

        for i in self.screens:
            display = i.render()
            for nx, x in enumerate(display):
                for ny, y in enumerate(x):
                    pygame.draw.rect(self.screen, y,
                                     pygame.Rect(100 + nx * (i.pixel.x + 5), 500 - ny * (i.pixel.y + 5), i.pixel.x,
                                                 i.pixel.y))

    def cleanup(self):
        pygame.quit()

    def execute(self):
        if self.init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        self.cleanup()


class Screen:
    def __init__(self, size: Dimension, pixel: Dimension) -> None:
        self.size = size
        self.data = [[0 for i in range(size.x)] for j in range(size.y)]
        self.pixel = pixel

    def render(self):
        raise NotImplementedError()


class SpectrumVisual(Screen):
    def __init__(self, size: Dimension = Dimension(14, 20), pixel: Dimension = Dimension(25, 10),
                 sens: float = 0.035, topDelay: int = 0):

        self.findex = [0, A.indexFromFreq(30), A.indexFromFreq(60), A.indexFromFreq(90), A.indexFromFreq(120), A.indexFromFreq(170),
                A.indexFromFreq(220), A.indexFromFreq(410), A.indexFromFreq(600), A.indexFromFreq(800), A.indexFromFreq(1000),
                A.indexFromFreq(1500), A.indexFromFreq(2000), A.indexFromFreq(3750), A.indexFromFreq(4500)]

        self.sens = sens
        self.topDelay = topDelay
        super().__init__(size, pixel)
        self.addBand()
        self.calcBars()
        self.changePalette("beat")
        self.counter = 0

        # Colour Crossfade Variables
        self.crossfadeSpeed = 2
        self.r = 255
        self.g = 75
        self.b = 76

        # Beat Detection Variables
        self.beatDetectSensitivity = 2.2
        self.beatDetectThreshold = 12
        self.beatDetectionBar = 3
        self.beatDetect = [0 for i in range(20)]


    def calcBars(self):
        self.findex.sort()
        self.bar = []
        for i in range(len(self.findex) - 1):
            self.bar.append(self.sens * A.getSpectralBar(self.findex[i], self.findex[i + 1]))
        return

    def addBand(self, x=0):
        if x > 0: self.findex.append(A.indexFromFreq(x))
        self.tops = [[0, 0] for i in range((len(self.findex) - 1) * 2)]
        return

    def beatDetectColour(self):
        self.beatDetect.insert(0, self.bar[self.beatDetectionBar])
        self.beatDetect.pop()

        if self.beatDetect[0] > sum(self.beatDetect)/len(self.beatDetect) * self.beatDetectSensitivity and self.beatDetect[0] > self.beatDetectThreshold:
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
                self.r += 5
                self.g -= 5
            if self.g <= 75 and self.r > 75:
                self.g = 75
                self.r -= 5
                self.b += 5
            if self.r <= 75 and self.b > 75:
                self.r = 75
                self.g += 5
                self.b -= 5
        return [(min(max(self.r, 75), 240), min(max(self.g, 75), 240), min(max(self.b, 75), 240)) for i in
                range(self.size.y)]

    def peakingColours(self):
        res = []
        for j in range(self.size.y):
            if j > 17:
                res.append(red)
            elif j > 12:
                res.append(yellow)
            else:
                res.append(green)
        return res

    def gradient(self, c1, c2):
        res = []
        for i in range(self.size.y):
            res.append((
                c1[0] + i * (c2[0] - c1[0]) / 19,
                c1[1] + i * (c2[1] - c1[1]) / 19,
                c1[2] + i * (c2[2] - c1[2]) / 19
            ))
        return res

    def gradientCrossfadeColours(self):
        return self.gradient(self.crossfadeColours()[0], (
            self.crossfadeColours()[0][1], self.crossfadeColours()[0][0], self.crossfadeColours()[0][2]))

    def changePalette(self, x, *args):
        class InvalidPaletteException (Exception):
            """Raise when given invalid palette argument"""
            def __init__(self):
                super(InvalidPaletteException, self).__init__("Invalid palette argument")

        # self.beatDetectColour
        # self.crossfadeColours
        # self.peakingColours()
        # self.gradient(green, red)
        # self.gradientCrossfadeColours
        # self.beatDetectGradient

        if x == "peaking": self.palette = self.peakingColours()
        elif x == "beat": self.palette = self.beatDetectColour
        elif x == "gradient": self.palette = self.gradient(args[0], args[1])
        elif x == "cross": self.palette = self.crossfadeColours
        elif x == "gradientCross": self.palette = self.gradientCrossfadeColours
        elif x == "gradientBeat": self.palette = self.beatDetectGradient
        else: raise InvalidPaletteException

    def render(self):
        self.calcBars()

        self.counter += 1
        if callable(self.palette): col = self.palette()
        else: col = self.palette

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
                    t[self.tops[n][0]] = red
                    self.tops[n][1] += 1

            res.append(t)

        return res


purple = (128, 0, 128)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
cyan = (64, 224, 208)
black = (0, 0, 0)
white = (255, 255, 255)

A = AudioInput.AudioInput(4096, 96000, 4096, 1)

if __name__ == "__main__":
    w = Window(screens=(SpectrumVisual(), ), fpsLimiter=1)
    w.execute()
