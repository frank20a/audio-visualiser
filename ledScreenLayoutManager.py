from tkinter import *
from tkinter import filedialog, simpledialog
import json
import os
from multiprocessing import Queue
import queue

from customMenus import LedMenubar, LedToolbar, LedSidebar
from dimension import Dimension
from customExceptions import *
from connections import ConsoleConn

with open('ledScreenLayoutManager.info', 'r', encoding="utf8") as f:
    info = json.load(f)


class Node:
    def __init__(self, posx: int, posy: int):
        self.child = None
        self.pos = (posx, posy)

    def setChild(self, value: tuple = (0, 0, 0)):
        self.child = Node(value)

    def setVal(self, value: tuple = (0, 0, 0)):
        self.val = value

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
        print("Test")

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
                print(pos[0], i)
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


class LedCanvas(Canvas):
    def __init__(self, root):
        self.px = 25
        self.root = root

        super().__init__(root, width=self.root.canvasSize.x * self.px, height=self.root.canvasSize.y * self.px,
                         bg='black')

        self.bind("<Button-1>", self.clickCallback)

    def begin(self):
        self.config(width=self.root.canvasSize.x * self.px, height=self.root.canvasSize.y * self.px)

        self.delete(ALL)

        for i in range(1, self.root.canvasSize.x):
            self.create_line(0, i * self.px, self.root.canvasSize.y * self.px + 2, i * self.px, fill="lightgrey")
            self.create_line(i * self.px, 0, i * self.px, self.root.canvasSize.x * self.px + 2, fill="lightgrey")

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
        self.create_rectangle(pos[0] * self.px + 2, pos[1] * self.px + 2, (pos[0] + 1) * self.px - 2,
                              (pos[1] + 1) * self.px - 2, fill=col)

    def drawLine(self, pos1, pos2):
        self.create_line((pos1[0] + 0.5) * self.px, (pos1[1] + 0.5) * self.px, (pos2[0] + 0.5) * self.px,
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
        x, y = event.x // self.px, event.y // self.px

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
        self.minsize(width=900, height=600)
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
        self.connection = ConsoleConn()

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
        self.ledCanvas.pack(anchor=NW)

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


def run(queue: Queue):
    app = App(queue)
    app.loop()
