import tkinter as tk
from tkinter import *
import customWidgets as cw


class SpectrumMenu(tk.Frame):
    def __init__(self, parent, screen):
        self.screen = screen
        tk.Frame.__init__(self, parent)

        tk.Label(self, text=self.screen.name).grid(row=0, column=0, columnspan=2)

        # Colour Mode Settings
        cw.ColourModeSettings(self, self.screen).grid(row=1, column=0, columnspan=2, sticky=W)

        # Delay Settings
        cw.DelaySettings(self, self.screen).grid(row=2, column=0, columnspan=2, sticky=W)

        # Sensitivity Settings
        cw.SensitivitySettings(self, self.screen).grid(row=3, column=0, columnspan=2, sticky=W)

        # Beat Detection Sensitivity Settings
        cw.BeatSensitivitySettings(self, self.screen).grid(row=4, column=0, columnspan=2, sticky=W)

        # Beat Detection Bar Settings
        cw.BeatBarSettings(self, self.screen).grid(row=5, column=0, sticky=W)

        # Beat Detection Threshold Settings
        cw.BeatThresholdSettings(self, self.screen).grid(row=5, column=1, sticky=W)

        # Colour Crossfade Sensitivity Settings
        cw.CrossfadeSpeedSettings(self, self.screen).grid(row=6, column=0, columnspan=2, sticky=W)


class LineMenu(tk.Frame):
    def __init__(self, parent, screen):
        self.screen = screen
        tk.Frame.__init__(self, parent)

        tk.Label(self, text=self.screen.name).grid(row=0, column=0)

        # Colour Mode Settings
        cw.ColourModeSettings(self, self.screen).grid(row=1, column=0, sticky=W)

        # Delay Settings
        cw.DelaySettings(self, self.screen).grid(row=2, column=0, sticky=W)

        # Sensitivity Settings
        cw.SensitivitySettings(self, self.screen).grid(row=3, column=0, sticky=W)

        # Beat Detection Sensitivity Settings
        cw.BeatSensitivitySettings(self, self.screen).grid(row=4, column=0, sticky=W)

        # Beat Detection Threshold Settings
        cw.BeatThresholdSettings(self, self.screen).grid(row=5, column=0, sticky=W)

        # Colour Crossfade Sensitivity Settings
        cw.CrossfadeSpeedSettings(self, self.screen).grid(row=6, column=0, sticky=W)

        # Changing Frequency Settings
        cw.BarFreqSettings(self, self.screen).grid(row=7, column=0, sticky=W)
