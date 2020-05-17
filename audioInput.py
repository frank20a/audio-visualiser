from math import cos, pi, floor
import pyaudio
import numpy as np
from scipy.fftpack import fft
import struct


class AudioInput:
    def __init__(self, chunk=4096, Fs=48000, Nfft=256, res=4):
        self.chunk = chunk
        self.Fs = Fs
        self.res = res  # 1 is highest
        self.Nfft = Nfft
        self.sig = np.zeros(self.chunk)
        self.SIG = np.zeros(self.Nfft)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.Fs, input=True, output=False,
                                  frames_per_buffer=self.chunk, input_device_index=2)

    # ========= DEPRECATED =========
    # def getSpectralBar(self, i1, i2):
    #     return sum(np.abs(self.SIG[i1:i2])) / np.abs((i2 - i1))
    # ==============================

    def getSpectralBar(self, i):
        return np.abs(self.SIG)[i]

    def indexFromFreq(self, F):
        return floor(F * self.Nfft / self.Fs)

    @classmethod
    def BlackmanWindow(cls, N, a0, a1, a2, a3):
        return list(map(lambda n: a0 - a1 * cos(2 * pi * n / N) + a2 * cos(4 * pi * n / N) + a3 * cos(6 * pi * n / N),
                        range(N)))

    def Nuttall(self):
        w = AudioInput.BlackmanWindow(len(self.sig), 0.3555768, 0.487396, 0.144232, 0.012604)
        self.sig = np.multiply(self.sig, w)

    def BlackmanHarris(self):
        w = AudioInput.BlackmanWindow(len(self.sig), 0.35875, 0.48829, 0.14128, 0.01168)
        self.sig = np.multiply(self.sig, w)

    def LPF(self, fc=500):
        H = np.concatenate((np.ones(fc), np.zeros(self.sig.size - fc)))
        return np.multiply(self.sig, H)

    def HPF(self, fc=0):
        fc = int(fc * self.chunk / self.Fs)
        H = np.concatenate((np.zeros(fc), np.ones(self.sig.size - fc)))
        return np.multiply(self.sig, H)

    def spectrum(self):
        return (4 / self.Nfft) * np.abs(self.SIG[0:int(self.Nfft / 2)])

    def getData(self):
        data = self.stream.read(self.chunk, exception_on_overflow=False)
        # self.sig = np.array(struct.unpack(str(self.chunk) + 'h', data))[::self.res] / 32767
        self.sig = np.frombuffer(data, dtype=np.float32)[::self.res]
        # self.BlackmanHarris()
        self.SIG = fft(self.sig, self.Nfft)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
