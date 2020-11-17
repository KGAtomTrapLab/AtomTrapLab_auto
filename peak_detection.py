import numpy as np
import scipy as sp
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, butter, lfilter, cheby2, buttord
from scipy.fft import fft, ifft
import logging

logging.basicConfig(filename="example.log", level=logging.DEBUG)


def import_data(data):
    """ Imports the data from a CSV text file  and returns it as a dataframe """
    try:
        df = pd.read_csv(data, header=None, sep="\t")
        df.columns = ["Saturated Absorption", "Fabry Perot", "Error", "NaN", "Voltage"]
        for i in range(3):
            df["Saturated Absorption"][i] = 0
        logging.debug(f"This is the input data frame {df.head()}")
        return df
    except:
        raise FileNotFoundError


def butterworth_filter(signal):
    """ Filters a signal using a butterworth filter returns the filtered signal """
    N = buttord(0.1, 0.16, 0.11, 2)
    a, b = butter(N[0], N[1])
    filtered = lfilter(a, b, signal)
    for i in range(30):
        filtered[i] = 0
    logging.info({"This is the filtered Sat Signal {}".format(filtered)})
    return filtered


def generate_all_attempts(peaks):
    """ Generates all 5 inorder peak combinations form a set of input peaks """
    attempts = []
    for i in range(len(peaks) % 5):
        attempts.append(peaks[i : (5 + i)])
    attempts = np.array(attempts)
    logging.info("These are the attempts {}".format(attempts))
    return attempts


def find_saturated_abs_peaks(signal):
    """ Finds the peaks in the saturated absorbtion data, returns an array of peak locations"""
    peaks, properties = find_peaks(signal, height=0.10)
    logging.info("These are the Sat Abs peaks {}".format(peaks))

    return peaks, properties


def find_error_peaks(signal):
    """ Find how many transitions in an error signal """
    peaks_error, properties_error = find_peaks(
        signal, prominence=(None, 0.3), height=0.10, wlen=100, distance=100
    )
    return peaks_error, properties_error


def error_filter(signal):
    """ Filter error signal. Takes in error signal and outputs the filtered signal """
    N = buttord(0.1, 0.12, 0.11, 2)
    a, b = butter(N[0], N[1])
    filtered = lfilter(a, b, signal)
    return filtered


def shift(peaks):
    """ Shifts peaks by set value """
    for i in range(len(peaks)):
        peaks[i] = peaks[i] - 6
    return peaks


def get_thumb(peaks):
    """ returns thumb of array """
    logging.debug("This is the thumb {}".format(peaks[-1]))
    return peaks[-1]


if __name__ == "__main__":
    df = import_data("testScan2.txt")
    filtered = butterworth_filter(df["Saturated Absorption"])
    peaks, properties = find_saturated_abs_peaks(filtered)
    peaks = shift(peaks)

    possible_combos = generate_all_attempts(peaks)

    error = error_filter(df["Error"])
    error_peaks, error_properties = find_error_peaks(error)

    plt.plot(error)
    plt.plot(error_peaks, error[error_peaks], "o")
    plt.plot(df["Saturated Absorption"])
    plt.plot(peaks, df["Saturated Absorption"][peaks], "x")
    plt.show()
