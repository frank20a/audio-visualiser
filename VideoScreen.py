import tkinter as tk
import cv2
import pickle
import os

from Screen import Screen
from Dimension import Dimension
from tkinter.filedialog import askopenfilename


class Video(Screen):
    number = 0

    def __init__(self, size: Dimension = Dimension(50, 40), pixel: Dimension = Dimension(5, 5), pxDist=0):
        self.name = self.__class__.__name__ + ' - ' + str(Video.number)
        Video.number += 1

        self.size = size
        self.pixel = pixel
        self.pxDist = pxDist
        super().__init__(size, pixel, pxDist)

        videoFile = askopenfilename(initialdir="/visuals", title="Select video file", filetypes=[('AVI files', '.avi'),
                                                                                                 ('MP4 files', '.mp4')])
        pickleFile = ''.join(videoFile.split('.')[:-1]) + '.frames'
        if os.path.isfile(pickleFile):
            self.frames = pickle.load(open(pickleFile, 'rb'))
        else:
            self.frames = []
            cap = cv2.VideoCapture(videoFile)
            if not cap.isOpened(): cap.open()
            fc = cap.get(7)
            i = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(i, fc)
                    i += 1
                    frame = cv2.resize(frame, tuple(self.size))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frames.append(frame.tolist())
                else:
                    break
            cv2.destroyAllWindows()
            cap.release()
            pickle.dump(self.frames, open(pickleFile, 'wb'))
        self.iter = 0
        self.vidLen = len(self.frames)

    def createSettings(self, parent):
        self.settings = tk.Frame(parent)
        return self.settings

    def render(self) -> list:
        self.iter += 1
        frame = self.frames[self.iter - 1]
        if self.iter == self.vidLen: self.iter = 0
        return frame

    def cleanup(self):
        print("Closed", self.name)
