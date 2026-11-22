import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
import matplotlib.pyplot as plt

TARGET_FS = 16000
F_LOW = 100.0
F_HIGH = 8000.0

def log_bands(n, f_low=F_LOW, f_high=F_HIGH):
    ratio = (f_high / f_low) ** (1 / n)
    edges = [f_low * ratio**k for k in range(n + 1)]
    edges[-1] = f_high  # avoid floating-point drift on the top edge
    return [[round(edges[k], 2), round(edges[k + 1], 2)] for k in range(n)]


def filter_bank(x, fs, bands, order=4):
    channels = []
    for lo, hi in bands:
        if hi >= fs / 2:
            sos = butter(order, lo, btype="highpass", fs=fs, output="sos")
        else:
            sos = butter(order, [lo, hi], btype="bandpass", fs=fs, output="sos")
        channels.append(sosfilt(sos, x))
    return channels


def split_channels(path, n):
    x, fs = sf.read(path)
    if fs != TARGET_FS:
        x = resample_poly(x, TARGET_FS, fs)
    return filter_bank(x, TARGET_FS, log_bands(n))


def plot_channel(y, title):
    t = np.arange(len(y)) / TARGET_FS
    plt.figure()
    plt.plot(t, y)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(alpha=0.3)

def rectify_channels(channels):
    return [np.abs(y) for y in channels]

channels = split_channels("audio/selected/child_quiet_1.wav", 8)
plot_channel(channels[0], "Lowest channel")
plot_channel(channels[-1], "Highest channel")
plt.show()
rectified = rectify_channels(channels)
