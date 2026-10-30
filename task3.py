import glob
import os
import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

TARGET_FS = 16000
TWO_MS = 2e-3
OUTPUT_DIR = "audio/output"
MONO_DIR = os.path.join(OUTPUT_DIR, "mono")
WAVEFORM_DIR = os.path.join(OUTPUT_DIR, "waveform")
COSINE_DIR = os.path.join(OUTPUT_DIR, "cosine")


def process_sound(path):
    x, fs = sf.read(path)
    print(f"{path}: sampling rate = {fs} Hz")

    if x.ndim == 2:
        x = x.mean(axis=1)

    if fs < TARGET_FS:
        print(f"{path}: {fs} Hz is below 16 kHz, pick a different file")
        return None

    sd.play(x, fs)
    sd.wait()

    name = os.path.splitext(os.path.basename(path))[0]
    sf.write(os.path.join(MONO_DIR, f"{name}_mono.wav"), x, fs)

    plt.figure()
    plt.plot(x)
    plt.title(f"Waveform: {path}")
    plt.xlabel("Sample number")
    plt.ylabel("Amplitude")
    plt.savefig(os.path.join(WAVEFORM_DIR, f"{name}_waveform.png"))

    if fs != TARGET_FS:
        x = resample_poly(x, TARGET_FS, fs)

    return x


def cosine_1khz(name, n):
    t = np.arange(n) / TARGET_FS
    y = np.cos(2 * np.pi * 1000 * t)

    sd.play(y, TARGET_FS)
    sd.wait()

    two = t <= TWO_MS
    plt.figure()
    plt.plot(t[two], y[two])
    plt.title("1 kHz cosine (two cycles)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.savefig(os.path.join(COSINE_DIR, f"{name}_cosine_1khz.png"))

    return y

for d in (MONO_DIR, WAVEFORM_DIR, COSINE_DIR):
    os.makedirs(d, exist_ok=True)
files = sorted(glob.glob("audio/selected/*.wav"))

for f in files:
    x = process_sound(f)
    if x is None:
        continue
    name = os.path.splitext(os.path.basename(f))[0]
    cosine_1khz(name, len(x))

plt.show()
