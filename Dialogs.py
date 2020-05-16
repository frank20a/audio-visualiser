from tkinter import *
from tkinter.ttk import *


class NewScreenDialog(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.minsize(width=250, height=10)
        self.title("Select Screen")

        self.var = ""

        Label(self, text="Select Screen Type").pack(anchor=NW, pady=20, padx=10)
        self.combo = Combobox(self, values=['Spectrum', 'SpectrumLine', 'ResponsiveStar', 'ResponsiveBox',
                                            'ResponsiveHelix', 'Video'])
        self.combo.pack(padx=10, fill=X)
        self.combo.current(0)

        b = Button(self, text="OK", command=self.ok, width=35)
        b.pack(pady=30, padx=20, anchor=SE)

    def ok(self):
        self.var = self.combo.get()
        if self.var != '':
            self.destroy()

    def show(self):
        try:
            self.wm_deiconify()
            self.combo.focus_force()
            self.wait_window()
            return self.var
        except Exception as e:
            return ""


class Progressbar(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.minsize(width=250, height=10)
        self.title("Select Screen")

        self.var = ""

        Label(self, text="Select Screen Type").pack(anchor=NW, pady=20, padx=10)
        self.combo = ttk.Combobox(self, values=['Spectrum', 'SpectrumLine', 'ResponsiveStar', 'ResponsiveBox',
                                                'ResponsiveHelix', 'Video'])
        self.combo.pack(padx=10, fill=X)
        self.combo.current(0)

        b = Button(self, text="OK", command=self.ok, width=35)
        b.pack(pady=30, padx=20, anchor=SE)

    def ok(self):
        self.var = self.combo.get()
        if self.var != '':
            self.destroy()

    def show(self):
        try:
            self.wm_deiconify()
            self.combo.focus_force()
            self.wait_window()
            return self.var
        except Exception as e:
            return ""
