from tkinter import *
from tkinter import filedialog, simpledialog
import json
import os
from multiprocessing import Queue
import queue

from Menus import LedMenubar, LedToolbar, LedSidebar
from Dialogs import ChooseConnDialog
from Dimension import Dimension
from Exceptions import *
import Connections as conn

with open('ledScreenLayoutManager.info', 'r', encoding="utf8") as f:
    info = json.load(f)


class Node:
    def __init__(self, posx: int, posy: int):
        self.child = None
        self.pos = (posx, posy)

    def setPos(self, posx, posy):
        self.pos = (posx, posy)

    def toDict(self):
        return {
            "posx": self.pos[0],
            "posy": self.pos[1]
        }


class LedList:
    def __init__(self, root: Node = None):
        self.root = root
        self.leaf = self.root

        self.positions = []
        if root is not None: self.positions.append(root.pos)
        self.fillPos = None

    def add(self, node: Node):
        if node.pos in self.positions: raise LedAlreadyPresent
        self.positions.append(node.pos)
        if self.root is None:
            self.root = node
            self.leaf = self.root
        else:
            while self.leaf.child is not None:
                self.leaf = self.leaf.child
            self.leaf.child = node
            self.leaf = self.leaf.child

    def empty(self, newRoot: Node):
        self.root = newRoot
        self.leaf = newRoot
        self.positions = [newRoot.pos]

    def read(self, filename: str = "untitled.ledlayout") -> tuple:
        with open(filename, 'r', encoding="utf8") as file:
            data = json.load(file)

        self.empty(Node(data['list'][0]['posx'], data['list'][0]['posy']))
        for i in data['list'][1:]: self.add(Node(i['posx'], i['posy']))

        return data['posx'], data['posy']

    def save(self, posx: int, posy: int, filename: str = "untitled.ledlayout"):
        t = []
        iter = self.root
        while iter is not None:
            t.append(iter.toDict())
            iter = iter.child
        with open(filename, 'w', encoding='utf8') as f:
            f.write(json.dumps({"posx": posx, "posy": posy, "list": t}))

    def strip(self, index) -> None:

        if self.root.child is None:
            self.positions.remove(self.root.pos)
            self.root = None
            self.leaf = self.root
            return

        iter = self.root
        if type(index) == int:
            for i in range(index):
                iter = iter.child
                if iter is None:
                    raise LedIndexError("Index: " + str(index) + "out of range")
            self.leaf = iter
            while iter is not None:
                self.positions.remove(iter.pos)
                iter = iter.child
            self.leaf.child = None

        elif type(index) == tuple:
            while iter is not None:
                if iter.pos == index:
                    self.leaf = iter
                    while iter.child is not None:
                        self.positions.remove(iter.child.pos)
                        iter = iter.child
                    self.leaf.child = None
                    return
                iter = iter.child
            raise LedIndexError("Position: " + str(index))
        else:
            raise InvalidIndexType("Type: " + str(type(index)))

    def remove(self, pos: tuple):
        if self.root.pos == pos:
            self.root = self.root.child
            self.positions.remove(pos)
            return
        iter = self.root
        while iter.child is not None:
            if iter.child.pos == pos:
                iter.child = iter.child.child
                self.positions.remove(pos)
                return
            iter = iter.child
        raise LedNotFound("Position: " + str(pos))

    def fill(self, pos: tuple):
        if pos in self.positions: raise LedAlreadyPresent

        if self.fillPos is None:
            self.fillPos = pos
            return

        if self.fillPos[0] == pos[0]:
            if self.fillPos[1] > pos[1]:
                step = -1
            else:
                step = +1

            for i in range(self.fillPos[1], pos[1] + step, step):
                # print(pos[0], i)
                self.add(Node(pos[0], i))
        elif self.fillPos[1] == pos[1]:
            if self.fillPos[0] > pos[0]:
                step = -1
            else:
                step = +1

            for i in range(self.fillPos[0], pos[0] + step, step):
                self.add(Node(i, pos[1]))

        self.fillPos = None

    def move(self, pos: tuple):
        pass


class LedCanvas(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.px = 25
        self.root = root

        # Create Canvas to attach scrollbars
        self.container = Canvas(self, borderwidth=0)
        # Create scrollable Frame
        self.frame = Frame(self.container)

        # Create Scrollbars
        h = Scrollbar(self, orient=HORIZONTAL, command=self.container.xview)
        self.container.configure(xscrollcommand=h.set)
        h.pack(side=BOTTOM, fill=X)
        v = Scrollbar(self, orient=VERTICAL, command=self.container.yview)
        self.container.configure(yscrollcommand=v.set)
        v.pack(side=RIGHT, fill=Y)

        # Pack containers
        self.container.pack(side='left', fill='both', expand=True)
        self.container.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        # Bind Configuration
        self.frame.bind("<Configure>", self.onFrameConfigure)

        # Create actual content
        self.canvas = Canvas(self.frame, width=self.root.canvasSize.x * self.px,
                             height=self.root.canvasSize.y * self.px, bg='black')
        self.canvas.bind("<Button-1>", self.clickCallback)
        self.canvas.pack(anchor=NW)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.container.configure(scrollregion=self.container.bbox("all"))

    def begin(self):
        self.canvas.config(width=self.root.canvasSize.x * self.px, height=self.root.canvasSize.y * self.px)

        self.canvas.delete(ALL)

        for i in range(1, self.root.canvasSize.x):
            self.canvas.create_line(i * self.px, 0, i * self.px, self.root.canvasSize.y * self.px + 2, fill="lightgrey")
        for i in range(1, self.root.canvasSize.y):
            self.canvas.create_line(0, i * self.px, self.root.canvasSize.x * self.px + 2, i * self.px, fill="lightgrey")

        if self.root.ledList.fillPos is not None: self.drawRec(self.root.ledList.fillPos, col='darkgrey')

        self.drawLayout()

    def pack(self, *args, **kwargs):
        super().pack(padx=4, pady=4, *args, **kwargs)
        self.begin()

    def zoom(self, amount):
        self.px = min(max(10, self.px + amount), 50)
        self.root.canvasSize = self.root.canvasSize
        self.begin()

    def drawRec(self, pos, col='blue'):
        if pos is None: raise NothingToDraw("Provided NoneType position. Can't draw there")

        pos = pos[0], self.root.canvasSize.y - pos[1] - 1
        self.canvas.create_rectangle(pos[0] * self.px + (2 if pos[0] != 0 else 3),
                                     pos[1] * self.px + (2 if pos[1] != 0 else 3),
                                     (pos[0] + 1) * self.px - (2 if pos[0] != self.root.canvasSize.x - 1 else 1),
                                     (pos[1] + 1) * self.px - (2 if pos[1] != self.root.canvasSize.y - 1 else 1),
                                     fill=col)

    def drawLine(self, pos1, pos2):
        pos1 = pos1[0], self.root.canvasSize.y - pos1[1] - 1
        pos2 = pos2[0], self.root.canvasSize.y - pos2[1] - 1
        self.canvas.create_line((pos1[0] + 0.5) * self.px, (pos1[1] + 0.5) * self.px, (pos2[0] + 0.5) * self.px,
                                (pos2[1] + 0.5) * self.px, fill="red", width=2)

    def drawLayout(self):
        class ListEmpty(Exception):
            """Tried to draw empty list"""
            pass

        try:
            iter = self.root.ledList.root
            if iter is None: raise ListEmpty
            self.drawRec(iter.pos, col='green')
            while iter.child is not None:
                self.drawRec(iter.child.pos)
                iter = iter.child

            iter = self.root.ledList.root
            while iter.child is not None:
                self.drawLine(iter.pos, iter.child.pos)
                iter = iter.child
        except ListEmpty as e:
            print(e)

    def clickCallback(self, event):
        x, y = event.x // self.px, self.root.canvasSize.y - event.y // self.px - 1

        try:
            if self.root.tool == 'add':
                self.root.ledList.add(Node(x, y))
            if self.root.tool == 'cut':
                self.root.ledList.strip((x, y))
            if self.root.tool == 'rem':
                self.root.ledList.remove((x, y))
            if self.root.tool == 'fill':
                self.root.ledList.fill((x, y))

        except (LedIndexError, LedNotFound) as e:
            print(e, "No LED there!")
        except LedAlreadyPresent:
            self.root.ledList.fillPos = None

        self.begin()


class App(Tk):
    def __init__(self, queue: Queue):
        super().__init__()

        # Window settings
        self.minsize(width=1100, height=700)
        self.maxsize(width=1100, height=700)
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        # self.state('zoomed')
        self.config(menu=LedMenubar(self))
        self.title(info["programName"])

        # Led List settings
        self.ledList = LedList()
        self.saveDir = ""

        # Toolbar settings
        self.toolbar = LedToolbar(self)
        self.sidebar = LedSidebar(self)

        # Canvas settings
        self.canvasSize = Dimension(0, 0)
        self.ledCanvas = LedCanvas(self)

        # Connection
        self.queue = queue
        self.transmitting = False
        self.connection = conn.Shredder(self)
        self.toolbar.transmit()

        self.packEverything()
        self.setTool("add")

        self.RUNNING = True

    # Core functionality
    def packEverything(self, tb=True, sb=True):
        self.toolbar.pack_forget()
        self.sidebar.pack_forget()
        self.ledCanvas.pack_forget()

        if tb: self.toolbar.pack()
        if sb: self.sidebar.pack()
        self.ledCanvas.pack(anchor=NW, expand=True, fill='both')

    def transmit(self):
        if self.transmitting:
            try:
                self.connection.transmit(self.queue.get_nowait())
            except queue.Empty:
                pass

    # Button callback functions
    def openLayout(self):
        ans = filedialog.askopenfilename(parent=self, initialdir=os.getcwd(), title="Select Layout File",
                                         filetypes=[('LED Layout files', '.ledlayout'), ('JSON files', '.json'),
                                                    ('All files', '.*')])
        self.saveDir = ans
        self.toolbar.saveBtn['state'] = NORMAL
        try:
            x, y = self.ledList.read(ans)
            self.canvasSize = Dimension(x, y)
            self.ledCanvas.begin()
        except Exception as e:
            self.saveDir = ''
            self.toolbar.saveBtn['state'] = DISABLED
            self.canvasSize = Dimension(0, 0)
            print(e)

    def saveAsLayout(self):
        ans = filedialog.asksaveasfilename(parent=self, initialdir=os.getcwd(), title="Select a filename for saving",
                                           filetypes=[('LED Layout files', '.ledlayout'), ('JSON files', '.json'),
                                                      ('All files', '.*')], defaultextension='.ledlayout')
        self.saveDir = ans
        self.toolbar.saveBtn['state'] = NORMAL
        try:
            self.ledList.save(self.canvasSize.x, self.canvasSize.y, ans)
        except Exception as e:
            self.saveDir = ''
            self.toolbar.saveBtn['state'] = DISABLED
            print(e)

    def saveLayout(self):
        if self.saveDir != '':
            try:
                self.ledList.save(self.canvasSize.x, self.canvasSize.y, self.saveDir)
            except Exception as e:
                print(e)
        else:
            self.toolbar.saveBtn['state'] = DISABLED
            raise SaveDirNotSet

    def newLayout(self):
        sizex = simpledialog.askinteger('Input X size', 'Provide width in number of pixels (LEDs): ', parent=self)
        if sizex is None: return
        sizey = simpledialog.askinteger('Input Y size', 'Provide height in number of pixels (LEDs): ', parent=self)
        if sizey is None: return

        self.saveDir = ''
        self.toolbar.saveBtn['state'] = DISABLED
        self.ledList = LedList()
        self.canvasSize = Dimension(sizex, sizey)
        self.ledCanvas.begin()

    def zoomIn(self):
        self.ledCanvas.zoom(5)

    def zoomOut(self):
        self.ledCanvas.zoom(-5)

    def setTool(self, tool):
        self.tool = tool
        for i in self.sidebar.buttons.values():
            i['state'] = NORMAL
        self.sidebar.buttons[tool]['state'] = DISABLED

    def connect(self):
        try:
            self.connection = [conn.Shredder, conn.ConsoleConn, conn.SerialConn, conn.NetworkTCPConn,
                               conn.NetworkUDPConn][ChooseConnDialog(self).show()](self)
        except TypeError:
            pass

    # Tk mainloop functions
    def loop(self):
        while self.RUNNING:
            self.toolbar.transLog.set("Connection: " + self.connection.type + "\nQueue overload: "
                                      + str(self.queue.qsize()))
            self.transmit()

            self.update()
        self.cleanup()

    def cleanup(self):
        pass

    def quit(self):
        self.RUNNING = False
        super().quit()
        self.destroy()


def run(queue: Queue):
    app = App(queue)
    app.loop()


if __name__ == "__main__":
    app = App(Queue())
    app.loop()
