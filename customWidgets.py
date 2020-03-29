import tkinter as tk
from tkinter import ttk
from tkinter import *


class ColourModeSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        tk.Label(self, text="Change Colour Mode").grid(row=0, column=0)
        self.colourCombo = ttk.Combobox(self, values=["peaking", "beat", "gradient", "cross", "gradientCross",
                                                      "gradientBeat"])
        self.colourCombo.grid(row=0, column=1, sticky=W)
        self.colourCombo.current(5)
        self.colourCombo.bind("<<ComboboxSelected>>", self.ColourModeSelected)
        self.colour1 = tk.Text(self, width=6, height=1)
        self.colour1.insert(tk.END, "000000")
        self.colour1.bind("<KeyRelease>", self.ColourModeSelected)
        self.colour1.grid(row=0, column=2)
        self.colour2 = tk.Text(self, width=6, height=1)
        self.colour2.insert(tk.END, "000000")
        self.colour2.bind("<KeyRelease>", self.ColourModeSelected)
        self.colour2.grid(row=0, column=3, sticky=E)

    def ColourModeSelected(self, event):
        try:
            c1 = self.colour1.get("1.0", "end-1c")
            c1 = (int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16))
            c2 = self.colour2.get("1.0", "end-1c")
            c2 = (int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16))
            self.screen.changePalette(self.colourCombo.get(), c1, c2)
        except:
            pass


class DelaySettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.delayVar = IntVar()
        self.delayCheck = tk.Checkbutton(self, text="Delay Tops", variable=self.delayVar, command=self.changeDelay)
        self.delayCheck.grid(row=0, column=0, columnspan=2, sticky=W)
        self.delayValText = tk.Text(self, width=2, height=1)
        self.delayValText.bind("<KeyRelease>", self.changeDelay)
        self.delayValText.grid(row=0, column=2, sticky=W)
        self.delayValText.insert(tk.END, str(self.screen.topDelay))
        if self.screen.topDelay > 0: self.delayCheck.invoke()

    def changeDelay(self, event=None):
        if self.delayVar.get():
            t = int(self.delayValText.get("1.0", "end-1c"))
            if t > 0:
                self.screen.topDelay = t
            else:
                self.delayValText.delete('1.0', tk.END)
                self.delayValText.insert(tk.END, "1")
                self.screen.topDelay = 1
        else:
            self.screen.topDelay = 0


class SensitivitySettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.sensitivityLabel = tk.Label(self, text="Sensitivity")
        self.sensitivityLabel.grid(row=0, column=0, sticky=SW)
        self.sensitivitySlider = tk.Scale(self, command=self.changeSensitivity, orient=HORIZONTAL, from_=0.001,
                                          to=0.1, resolution=0.001, showvalue=0, length=350,
                                          sliderlength=15)
        self.sensitivitySlider.set(self.screen.sens)
        self.sensitivitySlider.grid(row=0, column=1, columnspan=3, sticky=W)
        self.changeSensitivity()

    def changeSensitivity(self, event=None):
        self.screen.sens = self.sensitivitySlider.get()
        self.sensitivityLabel.config(text="Sensitivity: {0:4.3f}".format(self.sensitivitySlider.get()))


class BeatSensitivitySettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.beatSensitivityLabel = tk.Label(self, text="Beat Sensitivity")
        self.beatSensitivityLabel.grid(row=0, column=0, sticky=SW)
        self.beatSensitivitySlider = tk.Scale(self, command=self.changeBeatSensitivity, orient=HORIZONTAL,
                                              from_=3,
                                              to=1.5, resolution=0.05, showvalue=0, length=350,
                                              sliderlength=15)
        self.beatSensitivitySlider.set(self.screen.beatDetectSensitivity)
        self.beatSensitivitySlider.grid(row=0, column=1, columnspan=3, sticky=W)
        self.changeBeatSensitivity()

    def changeBeatSensitivity(self, event=None):
        self.screen.beatDetectSensitivity = self.beatSensitivitySlider.get()
        self.beatSensitivityLabel.config(text="Beat Sensitivity: {0:3.2f}".format(self.beatSensitivitySlider.get()))


class BeatBarSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.beatBarLabel = tk.Label(self, text="Detection Bar")
        self.beatBarLabel.grid(row=5, column=0, sticky=SW)
        self.beatBarSlider = tk.Scale(self, command=self.changeDetectionBar, orient=HORIZONTAL, from_=1,
                                      to=self.screen.size.x,
                                      resolution=1, showvalue=0, length=130, sliderlength=15)
        self.beatBarSlider.set(self.screen.beatDetectionBar)
        self.beatBarSlider.grid(row=5, column=1, sticky=W)
        self.changeDetectionBar()

    def changeDetectionBar(self, event=None):
        self.screen.beatDetectionBar = int(self.beatBarSlider.get()) - 1
        self.beatBarLabel.config(text="Detection Bar: {0}".format(int(self.beatBarSlider.get())))


class BeatThresholdSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.beatThreshLabel = tk.Label(self, text="Beat Threshold")
        self.beatThreshLabel.grid(row=5, column=2, sticky=SW)
        self.beatThreshSlider = tk.Scale(self, command=self.changeBeatThresh, orient=HORIZONTAL, from_=1,
                                         to=int(self.screen.size.y * 1.5),
                                         resolution=1, showvalue=0, length=100, sliderlength=15)
        self.beatThreshSlider.set(self.screen.beatDetectThreshold)
        self.beatThreshSlider.grid(row=5, column=3, sticky=W)
        self.changeBeatThresh()

    def changeBeatThresh(self, event=None):
        self.screen.beatDetectThreshold = int(self.beatThreshSlider.get()) - 1
        self.beatThreshLabel.config(text="Beat Threshold: {0:2}".format(int(self.beatThreshSlider.get())))


class CrossfadeSpeedSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.fadeSpeedLabel = tk.Label(self, text="Colour Fade Speed")
        self.fadeSpeedLabel.grid(row=6, column=0, sticky=SW)
        self.fadeSpeedSlider = tk.Scale(self, command=self.changeFadeSpeed, orient=HORIZONTAL, from_=15,
                                        to=1, resolution=1, showvalue=0, length=350, sliderlength=15)
        self.fadeSpeedSlider.set(self.screen.crossfadeSpeed)
        self.fadeSpeedSlider.grid(row=6, column=1, columnspan=3, sticky=W)
        self.changeFadeSpeed()

    def changeFadeSpeed(self, event=None):
        self.screen.crossfadeSpeed = int(self.fadeSpeedSlider.get())
        self.fadeSpeedLabel.config(text="Colour Fade Speed: {0}".format(int(self.fadeSpeedSlider.get())))