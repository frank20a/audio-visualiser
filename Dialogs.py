from tkinter.messagebox import showerror
from tkinter import *
from tkinter.ttk import *
import ipaddress


class NewScreenDialog(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.minsize(width=250, height=10)
        self.title("Select Screen")

        self.var = ""

        Label(self, text="Select Screen Type").pack(anchor=NW, pady=20, padx=10)
        self.combo = Combobox(self, values=['Spectrum', 'SpectrumBar', 'ResponsiveStar', 'ResponsiveBox',
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
        self.combo.current(len(COMs)-1)

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


class NetworkConnDialog(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.minsize(width=300, height=10)
        self.title("Configure Connection")
        self.root = root

        Label(self, text="Configure TCP Connection").pack(pady=20, padx=20, anchor=W)

        entries = Frame(self)
        Label(entries, text="IPv4:").pack(side=LEFT, padx=5)
        self.ip = StringVar()
        self.ip.set("192.168.1.")
        self.ip.trace('w', self.check_ip)
        self.ip_entry = Entry(entries, textvariable=self.ip, width=15)
        self.ip_entry.pack(side=LEFT, padx=5)

        Label(entries, text='Port:').pack(side=LEFT, padx=5)
        self.port = StringVar()
        self.port.set("25566")
        Entry(entries, textvariable=self.port, width=6).pack(side=LEFT, padx=5)
        entries.pack(pady=20, padx=20, anchor=W)

        b = Button(self, text="OK", command=self.ok, width=10)
        b.pack(pady=30, padx=20, anchor=SE)

    def check_ip(self, *args):
        temp = self.ip.get()
        # if len(temp) in (3, 7, 11):
        #     self.ip_entry.insert(END, '.')
        if len(temp) >= 15: self.ip.set(temp[:15])

    def ok(self):
        ip = self.ip.get()
        port = self.port.get()
        try:
            ip = ipaddress.ip_address(ip)
            self.res = (ip, port)
            self.destroy()
        except ValueError:
            showerror("Invalid IP Address", "The IP you provided is not a valid IPv4 address!", parent=self)
            self.ip.set("")


    def show(self):
        try:
            self.wm_deiconify()
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
        self.combo = Combobox(self, values=["Shredder", "Console", "Serial", "Network-TCP", "Network-UDP"])
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