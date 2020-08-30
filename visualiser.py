# Audio Visualiser by Frank Fourlas is licensed under CC BY-NC-SA 4.0.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0

import pygame
from time import time
import os
import tkinter as tk
from tkinter import *
import json
from multiprocessing import Process, Queue

import AudioInput
from Spectrums import Spectrum, SpectrumBar, SpectrumLine
from Boxes import ResponsiveStar, ResponsiveBox, ResponsiveHelix
from VideoScreen import Video
from Sensors import BeatDetectorTCP

from Colors import *
import Widgets as cw
from Menus import VisualiserMenubar
from Dialogs import NewScreenDialog
import ledScreenLayoutManager
from Exceptions import *

with open('visualiser.info', 'r', encoding="utf8") as f:
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

    def updateSize(self, parent):
        self.width, self.height = (len(self.screens) - 1) * 10, 0
        for i in self.screens:
            self.width += i.resolution.x
            self.height = max(self.height, i.resolution.y)

        self.width, self.height = max(self.width, 125), max(self.height, 40)
        self.size = self.width, self.height

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        parent.frame.config(width=self.width, height=self.height)

    def cleanup(self):
        for i in self.screens:
            i.cleanup()
        pygame.quit()


class Application(tk.Tk):
    def __init__(self, window: Window, *args, **kwargs):
        # Initiating tkinter application
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title(info['programName'] + ' v' + info['version'] + ' - by ' + info['author'])
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

        # Screen Settings Panel
        self.settingSelector = cw.SettingsPanel(self)
        self.settingSelector.pack(fill=X)
        self.SettingsContainer = cw.FrameWithWin(self, self.window)
        self.SettingsContainer.pack(fill=BOTH, expand=YES)
        self.config(menu=VisualiserMenubar(self))               # Needs to be after declaration of self.settingSelector
        self.settingsPanels = []

        # Create all the Frames for the settings panels
        for n, i in enumerate(self.window.screens):
            self.settingsPanels.append(i.createSettings(self.SettingsContainer))
            self.settingsPanels[-1].grid(row=0, column=0)
        self.settingSelector.selectSetting()

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
        elif cmd == "SpectrumBar":
            self.window.screens.append(SpectrumBar(self.window.audioDevice))
        elif cmd == "ResponsiveStar":
            self.window.screens.append(ResponsiveStar(self.window.audioDevice))
        elif cmd == "ResponsiveBox":
            self.window.screens.append(ResponsiveBox(self.window.audioDevice))
        elif cmd == "ResponsiveHelix":
            self.window.screens.append(ResponsiveHelix(self.window.audioDevice))
        elif cmd == "Video":
            self.window.screens.append(Video())

        self.settingsPanels.append(self.window.screens[-1].createSettings(self.SettingsContainer))
        self.settingsPanels[-1].grid(row=0, column=0)

        self.settingSelector.setCombobox()

        self.window.updateSize(self)
        self.config(menu=VisualiserMenubar(self))

        print("Created", self.window.screens[-1].name)

    def rmvScreen(self, screen):
        screen.cleanup()
        t = self.window.screens.index(screen)
        self.settingsPanels[t].destroy()
        self.settingsPanels.pop(t)
        self.window.screens.pop(t)

        self.settingSelector.setCombobox()

        self.window.updateSize(self)
        self.config(menu=VisualiserMenubar(self))

    def openLayoutManager(self):
        if not self.managerProc.is_alive():
            self.managerProc.start()


if __name__ == "__main__":
    A = AudioInput.AudioInput(4096, 96000, 4096 * 3, 1)
    app = Application(Window(A, screens=(SpectrumLine(A), BeatDetectorTCP(A),), fpsLimiter=1))
    app.open()
