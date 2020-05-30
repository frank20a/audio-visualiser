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


class SerialConnDialog(Toplevel):
    def __init__(self, root, COMs):
        super().__init__(root)
        self.minsize(width=300, height=10)
        self.title("Select COM")
        self.root = root

        self.COMs = COMs

        Label(self, text="Select Serial Communication Device").pack(anchor=NW, pady=20, padx=10)
        self.combo = Combobox(self, values=[str(i) for i in COMs])
        self.combo.pack(padx=10, fill=X)
        self.combo.current(1)

        Label(self, text="Select Baudrate").pack(anchor=NW, pady=20, padx=10)
        self.combo1 = Combobox(self, values=[300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 74880, 115200, 230400,
                                             250000, 500000, 1000000, 2000000])
        self.combo1.pack(padx=10, fill=X)
        self.combo1.current(11)

        b = Button(self, text="OK", command=self.ok, width=10)
        b.pack(pady=30, padx=20, anchor=SE)

    def ok(self):
        port = self.combo.current()
        rate = self.combo1.get()
        if port is not None and rate is not None:
            self.res = (self.COMs[port].device, rate)
            while not self.root.queue.empty(): self.root.queue.get_nowait()
            self.destroy()

    def show(self):
        try:
            self.wm_deiconify()
            self.combo.focus_force()
            self.wait_window()
            return self.res
        except Exception as e:
            return ""


class ChooseConnDialog(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.minsize(width=300, height=10)
        self.title("Select Connection")

        Label(self, text="Select Communication Method").pack(anchor=NW, pady=20, padx=10)
        self.combo = Combobox(self, values=["Shredder", "Console", "Serial", "TCP"])
        self.combo.pack(padx=10, fill=X)
        self.combo.current(0)

        b = Button(self, text="OK", command=self.ok, width=10)
        b.pack(pady=30, padx=20, anchor=SE)

    def ok(self):
        res = self.combo.current()
        if res is not None:
            self.res = res
            self.destroy()

    def show(self):
        try:
            self.wm_deiconify()
            self.combo.focus_force()
            self.wait_window()
            return self.res
        except Exception as e:
            return ""