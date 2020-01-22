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
black = (0, 0, 0)
r = 255
g = 1
b = 0

bar = []
fpsLimiter = 2  # Dictates that the screen is refreshed 3 times slower
topDelay = fpsLimiter * 0  # Good idea to make it a multiple of fpsLimiter
sens = 0.0375  # Limits the amplitude of the spectrum
btDtct = [False, False]
fps = 0


class Window:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 620, 600
        self.tops = [[0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green],
                     [0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green], [0, 0, green],
                     [0, 0, green], [0, 0, green]]
        self.color = (r, g, b)
        self.counter = 0

    def changeColourBtDtct(self):
        global r, g, b
        btDtct[0] = btDtct[1]
        if (bar[0] + bar[1]) / 2 > 16:
            btDtct[1] = True
        else:
            btDtct[1] = False

        if btDtct[0] and not btDtct[1]:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)

        self.color = (r, g, b)

    def fadeColours(self):
        global r, g, b
        if b <= 0 and g > 0:
            r = 0
            r += 10
            g -= 10
        if g <= 0 and r > 0:
            g = 0
            b += 10
            r -= 10
        if r <= 0 and b > 0:
            r = 0
            g += 10
            b -= 10
        self.color = (min(max(r, 75), 240), min(max(g, 75), 240), min(max(b, 75), 240))

    def on_init(self):
        global fps
        pygame.init()
        pygame.display.set_caption("Visualizer v0.1a")
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        global fps, bar, fpsLimiter, r, g, b, btDtct

        t = time()
        A.getData()
        bar = getBands()
        self.counter += 1

        if self.counter % fpsLimiter == 0: pygame.display.update()

        if self.counter % 2 == 0:
            try: fps = 1/((time() - t)*fpsLimiter)
            except: fps = 0

    def on_render(self):
        global bar, fps
        self.screen.fill(black)
        self.screen.blit(pygame.font.SysFont('Arial Bold', 30).render('FPS: %5.2f' % fps, False, red), (10, 10))

        for n, i in enumerate(bar):
            if topDelay > 0:
                if i > self.tops[n][0]:
                    self.tops[n][0] = min(int(i), 13)
                    self.tops[n][1] = 0
                    if i > 11:
                        self.tops[n][2] = red
                    elif i > 7:
                        self.tops[n][2] = yellow
                    else:
                        self.tops[n][2] = green
                if self.tops[n][1] % topDelay == 0: self.tops[n][0] -= 1

            for j in range(min(int(i) + 1, 14)):
                if j > 11:
                    self.color = red
                elif j > 7:
                    self.color = yellow
                else:
                    self.color = green

                self.changeColourBtDtct()

                pygame.draw.rect(self.screen, self.color, pygame.Rect(100 + n * 30, 500 - j * 30, 25, 25))

            if topDelay > 0 and self.tops[n][0] >= 0: pygame.draw.rect(self.screen, self.tops[n][2],
                        pygame.Rect(100 + n * 30, 500 - (1 + self.tops[n][0]) * 30, 25, 25))
            self.tops[n][1] += 1

    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


A = AudioInput.AudioInput(2048, 96000, 4096, 1)

# get indexes for frequencies
f = [0, A.indexFromFreq(150), A.indexFromFreq(250), A.indexFromFreq(500), A.indexFromFreq(1250),
     A.indexFromFreq(2000), A.indexFromFreq(2750), A.indexFromFreq(3500)]
print(f)


def getBands():
    res = []
    for i in range(len(f) - 1):
        # get 2 bands from each frequency range
        res.append(sens * A.getSpectralBar(f[i], (f[i] + f[i + 1]) // 2))
        res.append(sens * A.getSpectralBar((f[i] + f[i + 1]) // 2, f[i + 1]))
    return res


w = Window()
w.on_execute()
