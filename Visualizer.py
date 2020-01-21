import AudioInput
import pygame
from pygame.locals import *

purple = (128, 0, 128)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
b = []
topDelay = 4
sens = 0.04
counter = 0
fpsLimiter = 2

class Window:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 800, 600
        self.tops = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], ]

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        global b, counter, fpsLimiter
        A.getData()
        b = getBands()
        counter += 1
        if counter % fpsLimiter == 0: pygame.display.update()

    def on_render(self):
        global b
        self._display_surf.fill(black)
        for n, i in enumerate(b):
            if i > self.tops[n][0]:
                self.tops[n][0] = min(int(i), 13)
                self.tops[n][1] = 0
            if self.tops[n][1] % topDelay == 0: self.tops[n][0] -= 1

            for j in range(min(int(i)+1, 14)):
                if j > 11:
                    col = red
                elif j > 7:
                    col = yellow
                else:
                    col = green

                pygame.draw.rect(self._display_surf, col, pygame.Rect(100 + n * 30, 500 - j * 30, 25, 25))

            if self.tops[n][0] > 0: pygame.draw.rect(self._display_surf, red, pygame.Rect(100 + n * 30, 500 - (1+self.tops[n][0]) * 30, 25, 25))
            self.tops[n][1] += 1

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()



A = AudioInput.AudioInput(2048, 96000, 2048, 1)

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
