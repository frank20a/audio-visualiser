import pygame
from time import time
import os
import tkinter as tk
from tkinter import *

import audioInput
from spectrum import Spectrum, SpectrumLine
from boxes import ResponsiveStar, ResponsiveBox, ResponsiveHelix
from colors import *
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


class Application(tk.Tk):
    def __init__(self, window: Window, *args, **kwargs):
        # Initiating tkinter application
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self._running = True

        # Integrating pygame window
        self.window = window
        self.frame = tk.Frame(self, width=self.window.width, height=self.window.height)
        self.frame.pack(side=LEFT)
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Settings Panel
        settingSelector = cw.SettingsPanel(self, self.window)
        settingSelector.pack(fill=X)
        self.SettingsContainer = tk.Frame(self)
        self.SettingsContainer.pack(fill=BOTH, expand=YES)

        # Create all the Frames for the settings panels
        for n, i in enumerate(self.window.screens):
            i.createSettings(self.SettingsContainer).grid(row=0, column=0)

        settingSelector.selectSettingPanel()


    def open(self):
        self.window.init()
        while self._running:
            self.update()
            self.window.execute()

    def quit(self):
        self.window._running = False
        self._running = False
        self.destroy()


if __name__ == "__main__":
    A = audioInput.AudioInput(4096, 96000, 4096, 1)
    app = Application(Window(A, screens=(ResponsiveStar(A, size=20), ResponsiveHelix(A, size=20)), fpsLimiter=1))
    app.open()
