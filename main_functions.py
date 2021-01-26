import numpy as np
import scipy as sp
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks, butter, lfilter, cheby2, buttord
from scipy.fft import fft, ifft
from matplotlib.widgets import Cursor
import seaborn as sns
from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks
import math
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



def fabry_perot_conversions(fp_data,df,possible_combos):
    '''
    Takes fabry perot input data, finds free spectral range and converts the fsr from voltage to MHz/V. 
    Ouputs MHz per voltage conversion factor as well as the 10MHz conversion for trap transition tuning.
    possible_combos (arg) -> possible combination of peaks from the detected peaks in saturated absorption data.
    fp_peaks (output) - filtered peak indices of values within desired range.
    '''

    extended_range_factor = .20 
    conversions = []
    converted_trap= []
    peak_indices = find_peaks(fp_data)[0]
    peaks = np.array(list(zip(peak_indices, fp_data[peak_indices]))) #(index, value)
    threshold = 0.2 * max(fp_data[peak_indices])
    filtered_peaks = [(index, value) for index, value in peaks if value > threshold and index < 1000]

    # If you just want the indices:
    filtered_peak_indices = [index for index, value in peaks if value > threshold and index < 1000]

    for n in possible_combos:
        fp_range = (n[-1]-n[0])
        fp_start = n[0] - fp_range*(extended_range_factor)
        fp_end = n[-1] + fp_range*(extended_range_factor)
        peaks_in_range = []
        diffs = []
        fp_peaks = []
        for i in (filtered_peak_indices):
            if (i >= fp_start) and (i <= fp_end):
                voltage = df["Voltage"][i] #convert indices to voltage (x-axis on fabry perot)
                peaks_in_range.append(voltage)
                fp_peaks.append(i)
        for j in range(len(peaks_in_range)-1):
            difference = peaks_in_range[j+1]- peaks_in_range[j]
            diffs.append(difference)
        average_difference = sum(diffs)/len(diffs)
        conv = 300/average_difference   # 300MHz FSR, (MHz/V)
        q = (average_difference/300)*10   # 10MHz conversion for trap transition, unit: Voltage
        conversions.append(conv)
        converted_trap.append(q)
        
    return fp_peaks, conversions, converted_trap      
        


def raw_to_frequency_coords(raw_coords,conv,df):
    '''
    Convert raw coordinates to corresponding voltage values in dataframe. Outputs 
    voltage of each peak, from raw input.
    '''
    coords = []       
    for i in raw_coords:
        r = df.at[i,'Voltage']
        coords.append(r)
    c = []      # x-axis difference before conversion
    for i in coords:
        j = i - coords[0]
        c.append(j)
    # Difference after conversion (MHz/V)
    peak_freq = []      # frequency of peaks with first peak at 'zero' (in MHz)
    for i in c:
         dd = i*conv
         peak_freq.append(dd)
    return peak_freq


def frequency_percent_difference(peak_freq):
    '''
    Ouputs frequency data percent difference corresponding to the known values of the respective peaks. 
    With first peak at zero.
    '''
    Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition (MHz)
    Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump (MHz)
    Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2) (MHz)
    Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4) (MHz)
    while len(peak_freq) < 6: # Add zeroes to array until 'full.' 
        peak_freq.append((peak_freq[-1]+1))
    Rb87t_perc = []             # % Difference from transition - Rb 87 Trap
    for i in range(1, 6):
        R1 = (abs(peak_freq[i]-Rb87t[i])/(Rb87t[i]))*100
        Rb87t_perc.append(R1) 
    Rb87p_perc = []             # % Difference from transition - Rb87 pump
    for i in range(1, 6):
        R2 = (abs(peak_freq[i]-Rb87p[i])/(Rb87p[i]))*100
        Rb87p_perc.append(R2)
    Rb85t_perc = []             # % Difference from transition - Rb85 (2)
    for i in range(1, 6):
        R3 = (abs(peak_freq[i]-Rb85t[i])/(Rb85t[i]))*100
        Rb85t_perc.append(R3)
    Rb85_perc = []              # % Difference from transition - Rb85 (4)
    for i in range(1, 6):
        R4 = (abs(peak_freq[i]-Rb85[i])/(Rb85[i]))*100
        Rb85_perc.append(R4)
    return peak_freq, Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc


def frequency_intervals(peak_freq):
    '''
    Outputs the frequency interval between peaks. If the the input peaks are not in increasing order, 
    the loop breaks. There are two outputs. First (interval) is in the form of a list, the second, 
    interval_col is the same data as a dataframe column.
    '''
    interval = []    
    for i in range(1, 6):
        k = peak_freq[i]-peak_freq[i-1]
        if k <= 0:
            print('Peak interval of indices,(%.1f) - (%.1f) is not in increasing order.'%(i,i-1)) 
            break
        else:
            interval.append(k)
    interval_col = pd.DataFrame({'Intervals': interval})
    return interval


def interval_percent_difference(interval):
    '''
    Outputs the data intervals between peaks percent difference with respect to the known data values.
    
    '''
    Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition (MHz)
    Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump (MHz)
    Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2) (MHz)
    Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4) (MHz)
    Rb87t_pint = []         # Rb 87 Trap
    for i in range(0, 5):
        R1 = (abs(interval[i]-(Rb87t[i+1]-Rb87t[i]))/(Rb87t[i+1]-Rb87t[i]))*100
        Rb87t_pint.append(R1)
    Rb87p_pint = []         # Rb87 Pump
    for i in range(0, 5):
        R2 = (abs(interval[i]-(Rb87p[i+1]-Rb87p[i]))/(Rb87p[i+1]-Rb87p[i]))*100
        Rb87p_pint.append(R2)
    Rb85t_pint = []         # Rb85 (2)
    for i in range(0, 5):
        R3 = (abs(interval[i]-(Rb85t[i+1]-Rb85t[i]))/(Rb85t[i+1]-Rb85t[i]))*100
        Rb85t_pint.append(R3)
    Rb85_pint = []          # Rb85 (4)
    for i in range(0, 5):
        R4 = (abs(interval[i]-(Rb85[i+1]-Rb85[i]))/(Rb85[i+1]-Rb85[i]))*100
        Rb85_pint.append(R4)
    return Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint


def lowest_perc_diff(Rb87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc,Rb87t_pint, Rb87p_pint, Rb85t_pint, Rb85_pint):
    '''
    Input transition percent difference and interval percent difference from known values. 
    Outputs the transition. Outputs value to input into error_val function, whether to 
    output the error signal value shifted for trap transition or not.
    '''
    Rb87t = (Rb87t_perc)+(Rb87t_pint)
    Rb87p = (Rb87p_perc)+(Rb87p_pint)
    Rb85t = (Rb85t_perc)+(Rb85t_pint)
    Rb85 = (Rb85_perc)+(Rb85_pint)
    transition = 0
    if (Rb87t<Rb87p) and (Rb87t<Rb85t) and (Rb87t<Rb85):
        print("Rb87 Trap Transition")
        transition = 1
        return transition
    elif (Rb87p<Rb87t) and (Rb87p<Rb85t) and (Rb87p<Rb85):
        print("Rb87 Pump Transition")
        transition = 2
        return transition
    elif (Rb85t<Rb87t) and (Rb85t<Rb87p) and (Rb85t<Rb85):
        print("Rb85(2) Transition")
        transition = 3
        return transition
    elif (Rb85<Rb87t) and (Rb85<Rb87p) and (Rb85<Rb85t):
        print("Rb85(2) Transition")
        transition = 4
        return transition
    else:
        print('Lowest percent difference amongst input data was not calculated correctly')

        
def error_val(transition,raw_coords,df,q):
    '''
    Input what transition we are investigating:
        1 - Rb87 Trap Transition
        2 - Rb87 Pump Transition
        3 - Rb85 (2)
        4 - Rb85 (2)
        if trap transition, outputs the error signal value shifted left by ~10MHz voltage conversion, from fabry perot.
    '''
    #q is 10MHz conversion for trap transition, in units of voltage.
    if transition == 1:
        print("Trap Transition")
        error = df.at[raw_coords[-1],'Error'] - q  # q from fabry perot conversion function
    else:
        error = df.at[raw_coords[-1],'Error']
    return error
    

def percent_diff_heatmap(Rb87t_perc,Rb87p_perc,Rb85t_perc,Rb85_perc):
    # Percentage Heat Map (difference from transition)
    index= ['Peak 2', 'Peak 3', 'Peak 4', 'Peak 5', 'Peak 6']
    percentile_list = pd.DataFrame(
        {'Rb87 Trap': Rb87t_perc,
         'Rb87 Pump': Rb87p_perc,
         'Rb85 (2)': Rb85t_perc,
         'Rb85 (4)': Rb85_perc
        }, index = index)
    print(percentile_list)
    ax = plt.axes()
    sns.heatmap(percentile_list, cmap = 'ocean', annot = True, ax = ax)
    ax.set_title('Peaks')    
    plt.show()
    

def percent_int_heatmap(Rb87t_pint,Rb87p_pint,Rb85t_pint,Rb85_pint):
    # Interval Percentage Heat Map
    index= ['Interval 1', 'Interval 2', 'Interval 3', 'Interval 4', 'Interval 5']
    percentile_list2 = pd.DataFrame(
        {'Rb87 Trap': Rb87t_pint,
         'Rb87 Pump': Rb87p_pint,
         'Rb85 (2)': Rb85t_pint,
         'Rb85 (4)': Rb85_pint
        }, index = index)
    print(percentile_list2)
    ax = plt.axes()
    sns.heatmap(percentile_list2, cmap = 'ocean', annot = True, ax = ax)
    ax.set_title('Intervals')
    plt.show()




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
