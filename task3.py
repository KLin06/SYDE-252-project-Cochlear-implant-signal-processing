import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

TARGET_FS = 16000
TWO_MS = 2e-3


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

    sf.write(path.replace(".wav", "_mono.wav"), x, fs)

    plt.figure()
    plt.plot(x)
    plt.title(f"Waveform: {path}")
    plt.xlabel("Sample number")
    plt.ylabel("Amplitude")

    if fs != TARGET_FS:
        x = resample_poly(x, TARGET_FS, fs)

    return x


def cosine_1khz(n):
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

    return y

#"audio/sound.wav"
files = [] 

for f in files:
    x = process_sound(f)
    cosine_1khz(len(x))

plt.show()
