import tkinter as tk
from tkinter import *
import Widgets as cw


class SpectrumMenu(tk.Frame):
    def __init__(self, parent, screen):
        self.screen = screen
        self.parent = parent
        tk.Frame.__init__(self, parent)

        tk.Label(self, text=self.screen.name).grid(row=0, column=0, columnspan=2, pady=2)

        # Colour Mode Settings
        cw.ColourModeSettings(self, self.screen).grid(row=1, column=0, columnspan=2, sticky=W, pady=2)

        # Delay Settings
        cw.DelaySettings(self, self.screen).grid(row=2, column=0, columnspan=2, sticky=W, pady=2)

        # Sensitivity Settings
        cw.SensitivitySettings(self, self.screen).grid(row=3, column=0, columnspan=2, sticky=W, pady=2)

        # Beat Detection Sensitivity Settings
        cw.BeatSensitivitySettings(self, self.screen).grid(row=4, column=0, columnspan=2, sticky=W, pady=2)

        # Beat Detection Bar Settings
        cw.BeatBarSettings(self, self.screen).grid(row=5, column=0, sticky=W, pady=2)

        # Beat Detection Threshold Settings
        cw.BeatThresholdSettings(self, self.screen).grid(row=5, column=1, sticky=W, pady=2)

        # Colour Crossfade Sensitivity Settings
        cw.CrossfadeSpeedSettings(self, self.screen).grid(row=6, column=0, columnspan=2, sticky=W, pady=2)

        # Dimension Settings
        cw.DimensionChangeSettings(self, self.screen, self.screen.changeSize, title="Dimensions",
                                   placeholder=screen.size).grid(row=7, column=0, columnspan=2, sticky=W, pady=2)
        cw.DimensionChangeSettings(self, self.screen, self.screen.changePixel, title="Pixel Size",
                                   placeholder=screen.pixel).grid(row=8, column=0, columnspan=2, sticky=W, pady=2)
        cw.DimensionChangeSettings(self, self.screen, self.screen.changeDist, title="Pixel Distance",
                                   secondDimension=False, placeholder=screen.pxDist).grid(row=9, column=0, columnspan=2,
                                                                                          sticky=W, pady=2)


class LineMenu(tk.Frame):
    def __init__(self, parent, screen):
        self.screen = screen
        self.parent = parent
        tk.Frame.__init__(self, parent)

        tk.Label(self, text=self.screen.name).grid(row=0, column=0)

        # Colour Mode Settings
        cw.ColourModeSettings(self, self.screen).grid(row=1, column=0, sticky=W)

        # Delay Settings
        cw.DelaySettings(self, self.screen).grid(row=2, column=0, sticky=W)

        # SpectrumBar Direction Settings
        if str(type(screen)) == "<class 'Spectrums.SpectrumBar'>":
            cw.LineAlignSettings(self, self.screen).grid(row=3, column=0, sticky=W)

        # Sensitivity Settings
        cw.SensitivitySettings(self, self.screen).grid(row=4, column=0, sticky=W)

        # Beat Detection Sensitivity Settings
        cw.BeatSensitivitySettings(self, self.screen).grid(row=5, column=0, sticky=W)

        # Beat Detection Threshold Settings
        cw.BeatThresholdSettings(self, self.screen).grid(row=6, column=0, sticky=W)

        # Colour Crossfade Sensitivity Settings
        cw.CrossfadeSpeedSettings(self, self.screen).grid(row=7, column=0, sticky=W)

        # Changing Frequency Settings
        cw.BarFreqSettings(self, self.screen).grid(row=8, column=0, sticky=W)

        # Dimension Settings
        cw.DimensionChangeSettings(self, self.screen, self.screen.changeSize, title="Dimension", secondDimension=False,
                                   placeholder=screen.size.inverse()).grid(row=9, column=0, columnspan=2, sticky=W,
                                                                           pady=2)
        cw.DimensionChangeSettings(self, self.screen, self.screen.changePixel, title="Pixel Size",
                                   placeholder=screen.pixel).grid(row=10, column=0, columnspan=2, sticky=W, pady=2)
        cw.DimensionChangeSettings(self, self.screen, self.screen.changeDist, title="Pixel Distance",
                                   secondDimension=False, placeholder=screen.pxDist).grid(row=11, column=0, columnspan=2,
                                                                                          sticky=W, pady=2)


class BeatDetectorTCPMenu(tk.Frame):
    def __init__(self, parent, screen):
        self.screen = screen
        self.parent = parent
        tk.Frame.__init__(self, parent)

        tk.Label(self, text=self.screen.name).grid(row=0, column=0, columnspan=2, pady=5)

        # Changing Frequency Settings
        cw.BarFreqSettings(self, self.screen).grid(row=1, column=0, sticky=W, pady=5)

        # Dimension Settings
        cw.DimensionChangeSettings(self, self.screen, self.screen.changePixel, title="Pixel Size",
                                   placeholder=screen.pixel).grid(row=2, column=0, columnspan=2, sticky=W, pady=5)

        # Connection Settings
        tcpSet = cw.TCPSettings(self, self.screen)
        self.write_console = tcpSet.write_console
        tcpSet.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
