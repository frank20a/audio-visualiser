import AudioInput
import pygame
from random import randint
from time import time
from pygame.locals import *

purple = (128, 0, 128)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
cyan = (64, 224, 208)
black = (0, 0, 0)
r = 255; g = 75; b = 76

bar = []
fpsLimiter = 1  # Dictates that the screen is refreshed 3 times slower
topDelay = fpsLimiter * 0  # Good idea to make it a multiple of fpsLimiter
sens = 0.035  # Limits the amplitude of the spectrum
btDtct = [False, False]
fps = 0


class Window:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 620, 600
        self.addBand()
        self.counter = 0

    def addBand(self, x=0):
        global f
        if x > 0: f.append(A.indexFromFreq(2000))
        self.tops = [[0, 0] for i in range((len(f) - 1) * 2)]


    def beatDetectColour(self):
        global r, g, b
        btDtct[0] = btDtct[1]
        if (bar[2] + bar[3]) / 2 > 19:
            btDtct[1] = True
        else:
            btDtct[1] = False

        if btDtct[0] and not btDtct[1]:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)

        return [(min(max(r, 75), 240), min(max(g, 75), 240), min(max(b, 75), 240)) for i in range(20)]

    def beatDetectGradient(self):
        t = self.beatDetectColour()
        return self.gradient(t[0], (t[0][2], t[0][0], t[0][1]))

    def crossfadeColours(self):
        global r, g, b

        if self.counter % 4 == 0:
            if b <= 75 and g > 75:
                b = 75
                r += 5
                g -= 5
            if g <= 75 and r > 75:
                g = 75
                r -= 5
                b += 5
            if r <= 75 and b > 75:
                r = 75
                g += 5
                b -= 5
        return [(min(max(r, 75), 240), min(max(g, 75), 240), min(max(b, 75), 240)) for i in range(20)]

    def peakingColours(self):
        res = []
        for j in range(20):
            if j > 17:
                res.append(red)
            elif j > 12:
                res.append(yellow)
            else:
                res.append(green)
        return res

    def gradient(self, c1, c2):
        res = []
        for i in range(20):
            res.append((
                c1[0] + i * (c2[0] - c1[0]) / 19,
                c1[1] + i * (c2[1] - c1[1]) / 19,
                c1[2] + i * (c2[2] - c1[2]) / 19
            ))
        return res

    def gradientCrossfadeColours(self):
        return self.gradient(self.crossfadeColours()[0], (self.crossfadeColours()[0][1], self.crossfadeColours()[0][0],self.crossfadeColours()[0][2]))

    def init(self):
        global fps
        pygame.init()
        pygame.display.set_caption("Visualizer v0.1a")
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._running = True

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def loop(self):
        global fps, bar, fpsLimiter, r, g, b, btDtct

        t = time()
        A.getData()
        bar = getBands()
        self.N = len(bar)
        
        self.counter += 1

        if self.counter % fpsLimiter == 0:
            pygame.display.update()
            try:
                fps = 1 / ((time() - t) * fpsLimiter)
            except:
                fps = 0

    def render(self):
        global bar, fps
        self.screen.fill(black)
        self.screen.blit(pygame.font.SysFont('Arial Bold', 30).render('FPS: %5.2f' % fps, False, red), (10, 10))

        # self.beatDetectColour()
        # self.crossfadeColours()
        # self.peakingColours()
        # self.gradient(green, red)
        # self.gradientCrossfadeColours()
        # self.beatDetectGradient()
        palette = self.gradientCrossfadeColours()

        for n, i in enumerate(bar):
            if topDelay > 0:
                if i > self.tops[n][0]:
                    self.tops[n][0] = min(int(i), 20)
                    self.tops[n][1] = 0
                if self.tops[n][1] % topDelay == 0: self.tops[n][0] -= 1

            for j in range(min(int(i) + 1, 20)):
                pygame.draw.rect(self.screen, palette[j], pygame.Rect(100 + n * 30, 500 - j * 15, 25, 10))

            if topDelay > 0 and self.tops[n][0] >= 0: pygame.draw.rect(self.screen, red,
                                                                       pygame.Rect(100 + n * 30,
                                                                                   500 - (1 + self.tops[n][0]) * 15, 25,
                                                                                   10))
            self.tops[n][1] += 1

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


A = AudioInput.AudioInput(4096, 96000, 4096, 1)

# get indexes for frequencies
f = [0, A.indexFromFreq(60), A.indexFromFreq(120), A.indexFromFreq(220), A.indexFromFreq(600),
     A.indexFromFreq(1000), A.indexFromFreq(2000), A.indexFromFreq(4500)]


def getBands():
    f.sort()
    res = []
    for i in range(len(f) - 1):
        # get 2 bands from each frequency range
        res.append(sens * A.getSpectralBar(f[i], (f[i] + f[i + 1]) // 2))
        res.append(sens * A.getSpectralBar((f[i] + f[i + 1]) // 2, f[i + 1]))
    return res

if __name__ == "__main__":
    w = Window()
    w.execute()
        
