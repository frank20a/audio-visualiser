import tkinter as tk
from tkinter import ttk
from tkinter import *
from dimension import Dimension


class SettingsPanel(tk.Frame):
    def __init__(self, parent, window):
        tk.Frame.__init__(self, parent)

        self.window = window

        tk.Label(self, text="Settings for screen: ").pack(side=LEFT)
        self.settingsSelectorCombo = ttk.Combobox(self, values=[i.name for i in self.window.screens],
                                                  width=30)
        self.settingsSelectorCombo.bind("<<ComboboxSelected>>", self.selectSettingPanel)
        self.settingsSelectorCombo.current(0)
        self.settingsSelectorCombo.pack(side=LEFT)

        self.live = StringVar()
        self.live.set(self.settingsSelectorCombo.get())
        self.liveBtn = Radiobutton(self, text="LIVE", variable=self.live, value=self.settingsSelectorCombo.get(),
                                   state=DISABLED)
        self.liveBtn.pack(side=LEFT)

    def selectSettingPanel(self, event=None):
        self.window.screens[self.settingsSelectorCombo.current()].settings.tkraise()

        self.liveBtn['value'] = self.settingsSelectorCombo.get()

    def setCombobox(self):
        self.settingsSelectorCombo.delete(0, END)
        self.settingsSelectorCombo['values'] = tuple([i.name for i in self.window.screens])
        if len(self.window.screens) != 0:
            self.settingsSelectorCombo.current(0)
            self.selectSettingPanel()
        else:
            print("No screens")


class ColourModeSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        def limit(*args):
            temp = col1.get()
            if len(temp) > 6: col1.set(temp[:6])
            temp = col2.get()
            if len(temp) > 6: col2.set(temp[:6])

        col1 = StringVar()
        col1.trace('w', limit)
        col2 = StringVar()
        col2.trace('w', limit)

        tk.Label(self, text="Change Colour Mode").pack(side=LEFT, fill=X)
        self.colourCombo = ttk.Combobox(self, values=["peaking", "beat", "gradient", "cross", "gradientCross",
                                                      "gradientBeat"])
        self.colourCombo.pack(side=LEFT, padx=20)
        self.colourCombo.current(5)
        self.colourCombo.bind("<<ComboboxSelected>>", self.ColourModeSelected)

        Label(self, text="#").pack(side=LEFT)
        self.colour1 = tk.Entry(self, textvariable=col1, width=6)
        self.colour1.insert(tk.END, "000000")
        self.colour1.bind("<KeyRelease>", self.ColourModeSelected)
        self.colour1.pack(side=LEFT)

        Label(self, text="#").pack(side=LEFT)
        self.colour2 = tk.Entry(self, textvariable=col2, width=6)
        self.colour2.insert(tk.END, "000000")
        self.colour2.bind("<KeyRelease>", self.ColourModeSelected)
        self.colour2.pack(side=LEFT)

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
        self.delayCheck = tk.Checkbutton(self, text="Delay Tops     ", variable=self.delayVar,
                                         command=self.delayBtnHandler)
        self.delayCheck.grid(row=0, column=0, columnspan=2, sticky=W)
        if self.screen.topDelay > 0: self.delayCheck.invoke()

        self.delayValText = tk.Text(self, width=2, height=1)
        self.delayValText.bind("<KeyRelease>", self.changeDelay)
        self.delayValText.grid(row=0, column=2, sticky=W)
        self.delayValText.insert(tk.END, str(self.screen.topDelay))
        self.lbl1 = Label(self, text='Delay Time     ')
        self.lbl1.grid(row=0, column=3, sticky=W)

        self.delayDropFrameText = tk.Text(self, width=2, height=1)
        self.delayDropFrameText.bind("<KeyRelease>", self.changeDelay)
        self.delayDropFrameText.grid(row=0, column=4, sticky=W)
        self.delayDropFrameText.insert(tk.END, "1")
        self.lbl2 = Label(self, text='Drop Frames     ')
        self.lbl2.grid(row=0, column=5, sticky=W)

        self.fillDelayVar = IntVar()
        self.delayFillCheck = tk.Checkbutton(self, text="Fill Delay     ", variable=self.fillDelayVar,
                                             command=self.fillDelay)
        self.delayFillCheck.grid(row=0, column=6, columnspan=2, sticky=W)
        if self.screen.topDelay > 0: self.delayCheck.invoke()

        self.delayBtnHandler()

    def delayBtnHandler(self, event=None):
        t = self.delayVar.get()
        if t:
            self.delayValText["state"] = "normal"
            self.delayDropFrameText["state"] = "normal"
            self.delayFillCheck["state"] = "normal"
            self.lbl2["state"] = "normal"
            self.lbl1["state"] = "normal"
            self.changeDelay()
        else:
            self.delayValText["state"] = "disabled"
            self.delayDropFrameText["state"] = "disabled"
            self.delayFillCheck["state"] = "disabled"
            self.lbl2["state"] = "disabled"
            self.lbl1["state"] = "disabled"
            self.screen.topDelay = 0
            self.screen.topFrameDrop = 1

    def changeDelay(self, event=None):
        t = int(self.delayValText.get("1.0", "end-1c"))
        if t > 0:
            self.screen.topDelay = t
        else:
            self.delayValText.delete('1.0', tk.END)
            self.delayValText.insert(tk.END, "1")
            self.screen.topDelay = 1

        t = int(self.delayDropFrameText.get("1.0", "end-1c"))
        if t > 0:
            self.screen.topFrameDrop = t
        else:
            self.delayDropFrameText.delete('1.0', tk.END)
            self.delayDropFrameText.insert(tk.END, "1")
            self.screen.topFrameDrop = 1

    def fillDelay(self, event=None):
        t = self.fillDelayVar.get()
        self.screen.fillDelay = t
        self.delayDropFrameText.delete('1.0', END)

        if t:
            self.delayDropFrameText.insert(tk.END, "3")
        else:
            self.delayDropFrameText.insert(tk.END, "1")
        self.changeDelay()


class SensitivitySettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)

        self.screen = screen

        self.sensitivityLabel = tk.Label(self, text="Sensitivity")
        self.sensitivityLabel.grid(row=0, column=0, sticky=SW)
        self.sensitivitySlider = tk.Scale(self, command=self.changeSensitivity, orient=HORIZONTAL, from_=0.002,
                                          to=0.15, resolution=0.001, showvalue=0, length=350,
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


class BarFreqSettings(tk.Frame):
    def __init__(self, parent, screen):
        tk.Frame.__init__(self, parent)
        self.screen = screen

        tk.Label(self, text="Frequency: ").grid(column=0, row=0, padx=10)
        self.freq1 = tk.Text(self, width=6, height=1)
        self.freq1.insert(tk.END, str(self.screen.getFreq()))
        self.freq1.grid(column=1, row=0)
        tk.Button(self, text="Set", command=self.changeFreqs).grid(column=4, row=0, padx=10)
        self.freq1.bind("<KeyRelease>", self.changeFreqs())

    def changeFreqs(self):
        self.screen.addBand(int(self.freq1.get("1.0", "end-1c")))


class DimensionChangeSettings(tk.Frame):
    def __init__(self, parent, screen, callback, placeholder: Dimension = Dimension(0, 0), title: str = "",
                 xLim=float('inf'), yLim=float('inf'), secondDimension=True):
        tk.Frame.__init__(self, parent)
        self.screen = screen
        self.callback = callback
        self.parent = parent
        self.second = secondDimension

        def limit(*args):
            temp = self.xVar.get()
            if temp == '': temp = "0"
            if not temp.isalnum(): self.xVar.set(temp[:-1])
            if int(temp) > xLim: self.xVar.set(str(xLim))
            temp = self.yVar.get()
            if secondDimension and temp == '': temp = "0"
            if secondDimension and not temp.isalnum(): self.yVar.set(temp[:-1])
            if secondDimension and int(temp) > yLim: self.yVar.set(str(yLim))
        self.xVar = StringVar()
        self.yVar = StringVar()
        try:
            self.xVar.set(str(placeholder.x))
            self.yVar.set(str(placeholder.y))
        except AttributeError:
            self.xVar.set(str(placeholder))
            self.yVar.set('-')
        self.xVar.trace('w', limit)
        self.yVar.trace('w', limit)

        tk.Label(self, text=title).grid(column=0, row=0, padx=10)

        tk.Label(self, text="X:").grid(column=1, row=0)
        self.x = Entry(self, textvariable=self.xVar, width=5)
        self.x.grid(column=2, row=0, padx=5)
        tk.Label(self, text="Y:").grid(column=3, row=0)
        self.y = Entry(self, textvariable=self.yVar, width=5)
        self.y.grid(column=4, row=0, padx=5)
        if not secondDimension: self.y.config(state='disabled')
        Button(self, text="Set", command=self.set).grid(column=5, row=0, padx=15)

    def set(self, event=None):
        if self.second:
            try: x = int(self.xVar.get())
            except ValueError: x = 0

            try: y = int(self.yVar.get())
            except ValueError: y = 0

            self.callback(Dimension(x, y))
        else:
            try: x = int(self.xVar.get())
            except ValueError: x = 0

            self.callback(x)

        self.parent.parent.window.updateSize(self.parent.parent.parent)


class FrameWithWin(tk.Frame):
    def __init__(self, parent, window):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.window = window
