import numpy as np
import scipy as sp
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, butter, lfilter, cheby2, buttord
from scipy.fft import fft, ifft


def import_data(data):
    df = pd.read_csv("testScan2.txt", header=None, sep="\t")
    df.columns = ["Saturated Absorption", "NA", "Error", "NaN", "Voltage"]
    for i in range(3):
        df["Saturated Absorption"][i] = 0
    return df


def butterworth_filter(signal):
    N = buttord(0.1, 0.16, 0.11, 2)
    a, b = butter(N[0], N[1])
    filtered = lfilter(a, b, signal)
    for i in range(30):
        filtered[i] = 0
    return filtered


def generate_all_attempts(peaks):
    attempts = []
    for i in range(len(peaks) % 5):
        attempts.append(peaks[i : (5 + i)])
    attempts = np.array(attempts)
    return attempts


def find_saturated_abs_peaks(signal):
    peaks, properties = find_peaks(signal, height=0.10)
    return peaks, properties


def find_error_peaks(signal):
    peaks_error, properties_error = find_peaks(
        signal, prominence=(None, 0.3), height=0.10, wlen=100, distance=100
    )
    return peaks_error, properties_error


def error_filter(signal):
    N = buttord(0.1, 0.12, 0.11, 2)
    a, b = butter(N[0], N[1])
    filtered = lfilter(a, b, signal)
    return filtered


def shift(peaks):
    for i in range(len(peaks)):
        peaks[i] = peaks[i] - 6
    return peaks


def get_thumb(peaks):
    return peaks[-1]


if __name__ == "__main__":
    df = import_data("testScan2.txt")
    filtered = butterworth_filter(df["Saturated Absorption"])
    peaks, properties = find_saturated_abs_peaks(filtered)
    peaks = shift(peaks)

    possible_combos = generate_all_attempts(peaks)

    plt.plot(df["Saturated Absorption"])
    plt.plot(peaks, df["Saturated Absorption"][peaks], "x")
    plt.show()
