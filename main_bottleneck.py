import main_functions
from matplotlib import pyplot as plt
import numpy as np
'''
Import functions from peak_detection.py and heatmaps_function.py
INPUT:
    CSV Text file of data (columns must correspond)
        --> Must include(IN ORDER):
            "Saturated Absorption", "NA", "Error", "NaN", "Voltage"
            (1) Saturated Absorption
            (2) Fabry Perot
            (3) Error
            (4) NaN (Fabry Perot?)
            (5) Voltage
            Note-- Fabry Perot is input in the line:
                conv, q = heatmaps_function.fabry_perot_conversions(df["Fabry Perot"],df)
            
'''

def bottleneck(text_file):
    #df = peak_detection.import_data("testScan.txt")
    df = main_functions.import_data(text_file)
    # Imports the data from a CSV text file  and returns it as a dataframe
    
    filtered = main_functions.butterworth_filter(df["Saturated Absorption"])
    # Filters a signal using a butterworth filter returns the filtered signal
    peaks, properties = main_functions.find_saturated_abs_peaks(filtered)
    # Finds the peaks in the saturated absorbtion data, returns an array of peak locations
    peaks = main_functions.shift(peaks)
    # Shifts peaks by set value
    possible_combos = main_functions.generate_all_attempts(peaks)
    # Generates all 5 inorder peak combinations form a set of input peaks
    
    error = main_functions.error_filter(df["Error"])
    # Filter error signal. Takes in error signal and outputs the filtered signal
    error_peaks, error_properties = main_functions.find_error_peaks(error)
    # Find how many transitions in an error signal
    
    # print("CONVERSIONS")
    # print(conversions)
    
    fp_peaks, conversions, converted_trap = main_functions.fabry_perot_conversions(df["Fabry Perot"], df, possible_combos)
    # Takes fabry perot input data, finds free spectral range and converts the fsr from voltage to MHz/V. 
    # Ouputs MHz per voltage conversion factor as well as the 10MHz conversion for trap transition tuning.
    for i in range(len(possible_combos)):
        print("")
        print("Element %.0f in List of Possible Peaks"%(i+1))
        peak_freq = main_functions.raw_to_frequency_coords(possible_combos[i],conversions[i],df)
        # Convert raw coordinates to corresponding voltage values in dataframe. Outputs voltage of each peak, from raw input.
        peak_freq, Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc = main_functions.frequency_percent_difference(peak_freq)
        # Ouputs frequency data percent difference corresponding to the known values of the respective peaks. With first peak at zero.
        interval = main_functions.frequency_intervals(peak_freq) 	# interval_col also stored
        # Outputs the frequency interval between peaks.
        Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint = main_functions.interval_percent_difference(interval)
        # Outputs the data intervals between peaks percent difference with respect to the known data values.
        transition = main_functions.lowest_perc_diff(Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc,Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint)
        # Outputs the transition.
        main_functions.percent_diff_heatmap(Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc)
        # Percentage Heat Map (difference from transition)
        main_functions.percent_int_heatmap(Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint)
        # Interval Percentage Heat Map
        error_idx = main_functions.get_thumb(possible_combos[i])
        error_value = df["Voltage"][error_idx]
        print("Error Adjustment: ",error_value, "V")
        df.plot(x = "Voltage", y = "Saturated Absorption", legend=False, color = "g")
        plt.plot(df["Voltage"],error)
        plt.plot(df["Voltage"][error_idx], error[error_idx], "ro")
        plt.plot(df["Voltage"][peaks], df["Saturated Absorption"][peaks], "rx")
        plt.title("Trap Transition")
        plt.xlabel("Voltage [V]")
        plt.ylabel("Signal Voltage [V]")
        plt.legend(["Saturated Absorption", "Error Signal"])
        plt.grid()
        plt.hlines(0,-10,10,"r")
        plt.xticks(np.arange(-10, 10, step=1))
        plt.xlim(-10, 9)
        plt.show() 
        
        df.plot(x = "Voltage", y = "Fabry Perot", legend=False)
        plt.plot(df["Voltage"][fp_peaks], df["Fabry Perot"][fp_peaks], "rx")
        #plt.plot(df["Fabry Perot"][fp_peaks], "rx")
        plt.title("Fabry Perot")
        plt.xlabel("Voltage [V]")
        plt.ylabel("Signal Voltage [V]")
        plt.grid()
        plt.xticks(np.arange(-10, 10, step=1))
        plt.xlim(-10, 9)
        plt.show()  

    
    
    