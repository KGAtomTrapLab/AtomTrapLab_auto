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

# conv, q = fabry_perot_conversions(fp_data)
peak_freq = raw_to_frequency_coords(peaks,conv,df)
Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc = frequency_percent_difference(peak_freq)
interval = frequency_intervals(peak_freq) 	# interval_col also stored
Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint = interval_percent_difference(interval)
transition = lowest_perc_diff(Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc,Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint)
#error_val(transition,peaks,df,q)

percent_diff_heatmap(Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc)
percent_int_heatmap(Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint)