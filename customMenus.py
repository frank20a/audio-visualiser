from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
import json


def nothing():
    pass


class LedMenubar(Menu):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root;

        self.toolbarOn = BooleanVar()
        self.toolbarOn.set(1)
        self.sidebarOn = BooleanVar()
        self.sidebarOn.set(1)

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label='New Layout', command=self.root.newLayout)
        filemenu.add_command(label='Open Layout...', command=self.root.openLayout)
        filemenu.add_command(label='Save Layout As...', command=self.root.saveAsLayout)
        filemenu.add_command(label='Save Layout', command=self.root.saveLayout)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.root.quit)

        toolmenu = Menu(self, tearoff=0)
        toolmenu.add_radiobutton(label="Add Tool", command=lambda: self.root.setTool('add'))
        toolmenu.add_radiobutton(label="Fill Tool", command=lambda: self.root.setTool('fill'))
        toolmenu.add_radiobutton(label="Remove Tool", command=lambda: self.root.setTool('rem'))
        toolmenu.add_radiobutton(label="Cut Tool", command=lambda: self.root.setTool('cut'))
        toolmenu.add_radiobutton(label="Move Tool", command=lambda: self.root.setTool('move'))

        viewmenu = Menu(self, tearoff=0)
        viewmenu.add_command(label="Zoom In", command=self.root.zoomIn)
        viewmenu.add_command(label="Zoom Out", command=self.root.zoomOut)
        viewmenu.add_separator()
        viewmenu.add_checkbutton(label="Toolbar", onvalue=1, offvalue=0, variable=self.toolbarOn,
                                 command=self.toggleBar)
        viewmenu.add_checkbutton(label="Sidebar", onvalue=1, offvalue=0, variable=self.sidebarOn,
                                 command=self.toggleBar)

        connectmenu = Menu(self, tearoff=0)

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="About...", command=self.showInfo)

        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Tools", menu=toolmenu)
        self.add_cascade(label="View", menu=viewmenu)
        self.add_cascade(label="Connection", menu=connectmenu)
        self.add_cascade(label="Help", menu=helpmenu)

    def showInfo(self):
        with open('ledScreenLayoutManager.info', 'r', encoding="utf8") as f:
            info = json.load(f)

        messagebox.showinfo("About", info["programName"] + " v" + info["version"] + "\nCreated by " + info["author"] +
                            " in " + info["year"] + ".\nLicenced under " + info["licence"])

    def toggleBar(self, event=None):
        self.root.packEverything(self.toolbarOn.get(), self.sidebarOn.get())


class LedToolbar(Frame):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root, bd=1, relief=RAISED)

        newImg = PhotoImage(file="icons/New file.png")
        newBtn = Button(self, text="New Layout", image=newImg, relief=FLAT, compound=TOP,
                        command=self.root.newLayout)
        newBtn.image = newImg
        newBtn.pack(side=LEFT, pady=2, padx=2)

        openImg = PhotoImage(file="icons/Open.png")
        openBtn = Button(self, text="Open Layout...", image=openImg, relief=FLAT, compound=TOP,
                         command=self.root.openLayout)
        openBtn.image = openImg
        openBtn.pack(side=LEFT, pady=2, padx=2)

        saveAsImg = PhotoImage(file="icons/Save as.png")
        saveAsBtn = Button(self, text="Save Layout As...", image=saveAsImg, relief=FLAT, compound=TOP,
                           command=self.root.saveAsLayout)
        saveAsBtn.image = saveAsImg
        saveAsBtn.pack(side=LEFT, pady=2, padx=2)

        saveImg = PhotoImage(file="icons/Save.png")
        self.saveBtn = Button(self, text="Save Layout", image=saveImg, relief=FLAT, compound=TOP, state=DISABLED,
                              command=self.root.saveLayout)
        self.saveBtn.image = saveImg
        self.saveBtn.pack(side=LEFT, pady=2, padx=2)

        Separator(self, orient=VERTICAL).pack(side=LEFT, padx=4, fill=Y)

        zoomInImg = PhotoImage(file="icons/Zoom in.png")
        zoomInBtn = Button(self, text="Zoom In", image=zoomInImg, relief=FLAT, compound=TOP,
                           command=self.root.zoomIn)
        zoomInBtn.image = zoomInImg
        zoomInBtn.pack(side=LEFT, pady=2, padx=2)

        zoomOutImg = PhotoImage(file="icons/Zoom out.png")
        zoomOutBtn = Button(self, text="Zoom Out", image=zoomOutImg, relief=FLAT, compound=TOP,
                            command=self.root.zoomOut)
        zoomOutBtn.image = zoomOutImg
        zoomOutBtn.pack(side=LEFT, pady=2, padx=2)

        Separator(self, orient=VERTICAL).pack(side=LEFT, padx=4, fill=Y)

        connectImg = PhotoImage(file="icons/Monitors.png")
        connectBtn = Button(self, text="Connect", image=connectImg, relief=FLAT, compound=TOP,
                            command=nothing)
        connectBtn.image = connectImg
        connectBtn.pack(side=LEFT, pady=2, padx=2)

        closeImg = PhotoImage(file="icons/Close.png")
        closeBtn = Button(self, text="Close", image=closeImg, relief=FLAT, compound=TOP,
                          command=self.root.quit)
        closeBtn.image = closeImg
        closeBtn.pack(side=RIGHT, pady=2, padx=4)

        Separator(self, orient=VERTICAL).pack(side=RIGHT, padx=4, fill=Y)

    def pack(self, *args, **kwargs):
        super().pack(side=TOP, fill=X, *args, **kwargs)


class LedSidebar(Frame):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root, bd=1, relief=RAISED)

        addImg = PhotoImage(file="icons/Brush.png")
        addBtn = Button(self, text="Add Tool", image=addImg, relief=FLAT, compound=TOP,
                        command=lambda: self.root.setTool('add'))
        addBtn.image = addImg
        addBtn.pack(side=TOP, pady=2, padx=2)

        fillImg = PhotoImage(file="icons/Clear.png")
        fillBtn = Button(self, text="Fill Tool", image=fillImg, relief=FLAT, compound=TOP,
                         command=lambda: self.root.setTool('fill'))
        fillBtn.image = fillImg
        fillBtn.pack(side=TOP, pady=2, padx=2)

        remImg = PhotoImage(file="icons/Eraser.png")
        remBtn = Button(self, text="Rem Tool", image=remImg, relief=FLAT, compound=TOP,
                        command=lambda: self.root.setTool('rem'))
        remBtn.image = remImg
        remBtn.pack(side=TOP, pady=2, padx=2)

        cutImg = PhotoImage(file="icons/Cut.png")
        cutBtn = Button(self, text="Cut Tool", image=cutImg, relief=FLAT, compound=TOP,
                        command=lambda: self.root.setTool('cut'))
        cutBtn.image = cutImg
        cutBtn.pack(side=TOP, pady=2, padx=2)

        moveImg = PhotoImage(file="icons/Move.png")
        moveBtn = Button(self, text="Move Tool", image=moveImg, relief=FLAT, compound=TOP,
                         command=lambda: self.root.setTool('move'))
        moveBtn.image = moveImg
        moveBtn.pack(side=TOP, pady=2, padx=2)

        Separator(self, orient=HORIZONTAL).pack(side=TOP, pady=4, fill=X)

        self.buttons = {"add": addBtn, "fill": fillBtn, "rem": remBtn, "cut": cutBtn, "move": moveBtn}

    def pack(self, *args, **kwargs):
        super().pack(side=LEFT, fill=Y, *args, **kwargs)
