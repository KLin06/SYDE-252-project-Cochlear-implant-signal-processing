import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

TARGET_FS = 16000
F_LOW = 100.0
F_HIGH = 8000.0


def log_bands(n, f_low=F_LOW, f_high=F_HIGH):
    """Split [f_low, f_high] into n logarithmically spaced [lo, hi] ranges."""
    ratio = (f_high / f_low) ** (1 / n)
    edges = [f_low * ratio**k for k in range(n + 1)]
    edges[-1] = f_high  # avoid floating-point drift on the top edge
    return [[round(edges[k], 2), round(edges[k + 1], 2)] for k in range(n)]


def filter_bank(x, fs, bands, order=4):
    """Filter x through one bandpass filter per [lo, hi] band. Returns a list of channel signals."""
    channels = []
    for lo, hi in bands:
        if hi >= fs / 2:
            # top edge is at Nyquist, where a bandpass is invalid, so use a highpass instead
            sos = butter(order, lo, btype="highpass", fs=fs, output="sos")
        else:
            sos = butter(order, [lo, hi], btype="bandpass", fs=fs, output="sos")
        channels.append(sosfilt(sos, x))
    return channels


def split_channels(path, n):
    """Task 5: read one mono file from Task 3 and return a list of n channel signals."""
    x, fs = sf.read(path)
    if fs != TARGET_FS:
        x = resample_poly(x, TARGET_FS, fs)
    return filter_bank(x, TARGET_FS, log_bands(n))

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

TARGET_FS = 16000
F_LOW = 100.0
F_HIGH = 8000.0


def log_bands(n, f_low=F_LOW, f_high=F_HIGH):
    """Split [f_low, f_high] into n logarithmically spaced [lo, hi] ranges."""
    ratio = (f_high / f_low) ** (1 / n)
    edges = [f_low * ratio**k for k in range(n + 1)]
    edges[-1] = f_high  # avoid floating-point drift on the top edge
    return [[round(edges[k], 2), round(edges[k + 1], 2)] for k in range(n)]


def filter_bank(x, fs, bands, order=4):
    """Filter x through one bandpass filter per [lo, hi] band. Returns a list of channel signals."""
    channels = []
    for lo, hi in bands:
        if hi >= fs / 2:
            # top edge is at Nyquist, where a bandpass is invalid, so use a highpass instead
            sos = butter(order, lo, btype="highpass", fs=fs, output="sos")
        else:
            sos = butter(order, [lo, hi], btype="bandpass", fs=fs, output="sos")
        channels.append(sosfilt(sos, x))
    return channels


def split_channels(path, n):
    """Task 5: read one mono file from Task 3 and return a list of n channel signals."""
    x, fs = sf.read(path)
    if fs != TARGET_FS:
        x = resample_poly(x, TARGET_FS, fs)
    return filter_bank(x, TARGET_FS, log_bands(n))

def rectify_channels(channels):
    return [np.abs(y) for y in channels]

channels = split_channels("audio/selected/child_quiet_1.wav", 8)
rectified = rectify_channels(channels)
print(len(channels), "channels of", len(channels[0]), "samples")