import pygame
from time import time
import os
import tkinter as tk
from tkinter import *
import json
from multiprocessing import Process, Queue

import audioInput
from spectrum import Spectrum, SpectrumLine
from boxes import ResponsiveStar, ResponsiveBox, ResponsiveHelix
from videoScreen import Video
from colors import *
import Widgets as cw
from Menus import VisualiserMenubar
from Dialogs import NewScreenDialog
import ledScreenLayoutManager
from Exceptions import *

with open('ledScreenLayoutManager.info', 'r', encoding="utf8") as f:
    info = json.load(f)


class Window:
    def __init__(self, audioDevice, screens: tuple = (), fpsLimiter=1):
        self.audioDevice = audioDevice

        self.fpsLimiter = fpsLimiter
        self.screens = list(screens)
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
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

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

    def render(self, live: str):
        self.screen.fill(black)
        liveData = None

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
                        print(e, y)
            tempX += i.resolution.x + 10

            if i.name == live: liveData = display

        self.screen.blit(pygame.font.SysFont('Arial Bold', 30).render('FPS: %5.2f' % self.fps, False, red), (10, 10))

        return liveData

    def execute(self, live: str):
        if self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            return self.render(live)
        else:
            self.cleanup()

    def updateSize(self):
        self.width, self.height = (len(self.screens) - 1) * 10, 0
        for i in self.screens:
            self.width += i.resolution.x
            self.height = max(self.height, i.resolution.y)
        self.size = self.width, self.height

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    def cleanup(self):
        for i in self.screens:
            i.cleanup()
        pygame.quit()


class Application(tk.Tk):
    def __init__(self, window: Window, *args, **kwargs):
        # Initiating tkinter application
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title(info['programName'])
        self.config(menu=VisualiserMenubar(self))
        self._running = True

        # Define LED Screen Layout module
        self.queue = Queue()
        self.managerProc = Process(target=ledScreenLayoutManager.run, args=(self.queue,))

        # Integrating pygame window
        self.window = window
        self.frame = tk.Frame(self, width=self.window.width, height=self.window.height)
        self.frame.pack(side=LEFT)
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Settings Panel
        self.settingSelector = cw.SettingsPanel(self, self.window)
        self.settingSelector.pack(fill=X)
        self.SettingsContainer = tk.Frame(self)
        self.SettingsContainer.pack(fill=BOTH, expand=YES)

        # Create all the Frames for the settings panels
        for n, i in enumerate(self.window.screens):
            i.createSettings(self.SettingsContainer).grid(row=0, column=0)
        self.settingSelector.selectSettingPanel()

    def open(self):
        self.window.init()
        while self._running:
            self.update()
            data = self.window.execute(self.settingSelector.live.get())

            try:
                if not self.managerProc.is_alive():
                    self.settingSelector.liveBtn['state'] = DISABLED
                else:
                    self.settingSelector.liveBtn['state'] = NORMAL
            except tk.TclError:
                pass
            if data is not None: self.queue.put_nowait(data)

    def quit(self):
        if self.managerProc.is_alive(): self.managerProc.terminate()
        self.window._running = False
        self._running = False
        self.destroy()

    def addScreen(self):
        cmd = NewScreenDialog(self).show()
        if cmd == "Spectrum":
            self.window.screens.append(Spectrum(self.window.audioDevice))
        elif cmd == "SpectrumLine":
            self.window.screens.append(SpectrumLine(self.window.audioDevice))
        elif cmd == "ResponsiveStar":
            self.window.screens.append(ResponsiveStar(self.window.audioDevice))
        elif cmd == "ResponsiveBox":
            self.window.screens.append(ResponsiveBox(self.window.audioDevice))
        elif cmd == "ResponsiveHelix":
            self.window.screens.append(ResponsiveHelix(self.window.audioDevice))
        elif cmd == "Video":
            self.window.screens.append(Video())

        self.window.screens[-1].createSettings(self.SettingsContainer).grid(row=0, column=0)
        self.settingSelector.settingsSelectorCombo['values'] += (self.window.screens[-1].name,)
        self.settingSelector.selectSettingPanel()
        self.window.updateSize()
        self.frame.config(width=self.window.width, height=self.window.height)

    def openLayoutManager(self):
        if not self.managerProc.is_alive():
            self.managerProc.start()


if __name__ == "__main__":
    A = audioInput.AudioInput(4096, 96000, 4096 * 3, 1)
    app = Application(Window(A, screens=(SpectrumLine(A),), fpsLimiter=1))
    app.open()
