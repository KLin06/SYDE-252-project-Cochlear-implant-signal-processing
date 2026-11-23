import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
import matplotlib.pyplot as plt

TARGET_FS = 16000
F_LOW = 100.0
F_HIGH = 8000.0

# split the channel into n bands of doubling bandwidth
def log_bands(n, f_low=F_LOW, f_high=F_HIGH):
    ratio = (f_high / f_low) ** (1 / n)
    edges = [f_low * ratio**k for k in range(n + 1)]
    edges[-1] = f_high  
    return [[round(edges[k], 2), round(edges[k + 1], 2)] for k in range(n)]

# Default butterworth filter with a fourth order cutoff
def filter_bank(x, fs, bands, order=4):
    channels = []
    for lo, hi in bands:
        if hi >= fs / 2:
            sos = butter(order, lo, btype="highpass", fs=fs, output="sos")
        else:
            sos = butter(order, [lo, hi], btype="bandpass", fs=fs, output="sos")
        channels.append(sosfilt(sos, x))
    return channels

# Split the input sound into n channels
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


# Split the signal into 8 frequency bands, spaced logarithmically from
# 100 Hz to 8 kHz.
#
# Why 8 bands: speech recognition with cochlear-implant-style processing
# levels off at around 8 channels (Friesen et al., 2001; Shannon et al.,
# 1995). 
#
# Band width: the full range covers log2(8000 / 100) ≈ 6.32 octaves.
# Splitting that into 8 log-spaced bands makes each band about 0.79 of an
# octave wide (a ratio of 2^0.79 ≈ 1.73 between each band's upper and
# lower edge). The ear's frequency resolution works on a roughly
# logarithmic scale, so log spacing puts more bands in the low-to-mid
# range, where most speech cues are.

channels = split_channels("audio/selected/child_quiet_1.wav", 8)
plot_channel(channels[0], "Lowest channel")
plot_channel(channels[-1], "Highest channel")
plt.show()
rectified = rectify_channels(channels)
