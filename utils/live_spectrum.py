import numpy as np
import AudioInput
import matplotlib.pyplot as plt

A = AudioInput.AudioInput(2048, 48000, 1024, 1)

if __name__ == '__main__':
    # Plotting work
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    ax1.set_ylim(-1, 1)
    ax1.set_title("Input")
    ax2.set_ylim(0, 1/A.res)
    ax2.set_xlim(20, A.Fs / (2*A.res))
    ax2.set_title("Spectrum")

    t1 = np.arange(0, A.chunk)[::A.res]
    f = np.linspace(0, A.Fs / (2*A.res), int(A.Nfft/2))

    s = np.zeros(int(A.chunk/A.res))
    S = np.zeros(int(A.Nfft/2))

    line1, = ax1.plot(t1, s, '-', lw=2)
    line2, = ax2.plot(f, S, '-', lw=2)

    # Plotting Data Input
    while True:
        A.getData()

        line1.set_ydata(A.sig)
        line2.set_ydata(A.spectrum())

        fig.canvas.draw()
        fig.canvas.flush_events()
