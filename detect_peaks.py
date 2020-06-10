import numpy as np
import scipy as sp
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, butter, lfilter, cheby2, buttord
from scipy.fft import fft, ifft
import logging
import seaborn as sns
from matplotlib.widgets import Cursor
import peak_detection
import heatmaps_function


df = peak_detection.import_data("D0046rb87 peak 7292011 scan 2.txt")
filtered = peak_detection.butterworth_filter(df["Saturated Absorption"])
peaks, properties = peak_detection.find_saturated_abs_peaks(filtered)
peaks = peak_detection.shift(peaks)

possible_combos = peak_detection.generate_all_attempts(peaks)

error = peak_detection.error_filter(df["Error"])
error_peaks, error_properties = peak_detection.find_error_peaks(error)

plt.plot(error)
plt.plot(error_peaks, error[error_peaks], "o")
plt.plot(df["Saturated Absorption"])
plt.plot(peaks, df["Saturated Absorption"][peaks], "x")
plt.show()

conv, q = heatmaps_function.fabry_perot_conversions(df["NA"],df)

for peakset in possible_combos:
	peak_freq = heatmaps_function.raw_to_frequency_coords(peakset,conv,df)
	peak_freq, Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc = heatmaps_function.frequency_percent_difference(peak_freq)
	interval = heatmaps_function.frequency_intervals(peak_freq) 	# interval_col also stored
	Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint = heatmaps_function.interval_percent_difference(interval)
	transition = heatmaps_function.lowest_perc_diff(Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc,Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint)
	heatmaps_function.percent_diff_heatmap(Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc)
	heatmaps_function.percent_int_heatmap(Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint)
	error_value = heatmaps_function.error_val(transition,peaks,df,q)
	print("Error: ",error_value)