from matplotlib import pyplot as plt
import peak_detection
import heatmaps_function
'''
Import functions from peak_detection.py and heatmaps_function.py
INPUT:
    CSV Text file of data (columns must correspond)
        --> Must include(IN ORDER):
            "Saturated Absorption", "NA", "Error", "NaN", "Voltage"
            (1) Saturated Absorption
            (2) Fabry Perot
            (3) Error
            (4) NaN (Fabry Perot)
            (5) Voltage
            Note-- Fabry Perot is input in the line:
                conv, q = heatmaps_function.fabry_perot_conversions(df["NA"],df)
            
'''

df = peak_detection.import_data("D0046rb87 peak 7292011 scan 2.txt")
# Imports the data from a CSV text file  and returns it as a dataframe

filtered = peak_detection.butterworth_filter(df["Saturated Absorption"])
# Filters a signal using a butterworth filter returns the filtered signal
peaks, properties = peak_detection.find_saturated_abs_peaks(filtered)
# Finds the peaks in the saturated absorbtion data, returns an array of peak locations
peaks = peak_detection.shift(peaks)
# Shifts peaks by set value
possible_combos = peak_detection.generate_all_attempts(peaks)
# Generates all 5 inorder peak combinations form a set of input peaks

error = peak_detection.error_filter(df["Error"])
# Filter error signal. Takes in error signal and outputs the filtered signal
error_peaks, error_properties = peak_detection.find_error_peaks(error)
# Find how many transitions in an error signal

plt.plot(error)
plt.plot(error_peaks, error[error_peaks], "o")
plt.plot(df["Saturated Absorption"])
plt.plot(peaks, df["Saturated Absorption"][peaks], "x")
plt.show()

conv, q = heatmaps_function.fabry_perot_conversions(df["NA"],df)
# Takes fabry perot input data, finds free spectral range and converts the fsr from voltage to MHz/V. 
# Ouputs MHz per voltage conversion factor as well as the 10MHz conversion for trap transition tuning.

for peakset in possible_combos:
	peak_freq = heatmaps_function.raw_to_frequency_coords(peakset,conv,df)
    # Convert raw coordinates to corresponding voltage values in dataframe. Outputs voltage of each peak, from raw input.
	peak_freq, Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc = heatmaps_function.frequency_percent_difference(peak_freq)
    # Ouputs frequency data percent difference corresponding to the known values of the respective peaks. With first peak at zero.
	interval = heatmaps_function.frequency_intervals(peak_freq) 	# interval_col also stored
    # Outputs the frequency interval between peaks.
	Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint = heatmaps_function.interval_percent_difference(interval)
    # Outputs the data intervals between peaks percent difference with respect to the known data values.
	transition = heatmaps_function.lowest_perc_diff(Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc,Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint)
    # Outputs the transition.
	heatmaps_function.percent_diff_heatmap(Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc)
    # Percentage Heat Map (difference from transition)
	heatmaps_function.percent_int_heatmap(Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint)
    # Interval Percentage Heat Map
	error_value = heatmaps_function.error_val(transition,peaks,df,q)
	print("Error: ",error_value)