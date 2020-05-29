import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd
import seaborn as sns

def fabry_perot_conversions(fp_data):
    '''Takes fabry perot data, finds free spectral range and converts the fsr from voltage to MHz/V. Ouputs MHz per voltage conversion factor as well as the 10MHz conversion for trap transition tuning.'''
    # Difference = fp_data[i+1]-fp_data[i]
    # 300/Difference = conv     # 300MHz FSR, (MHz/V)
    # q = (Difference/300)*10   # 10MHz conversion for trap transition, unit: Voltage
    #return conv, q

def raw_to_frequency_coords(raw_coords,conv,df):
    '''Convert raw coordinates to corresponding voltage values in dataframe. Outputs voltage of each peak, from raw input.'''
    coords = []       
    for i in raw_coords:
        r = df.at[i[0],'Voltage']
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

# def known_transition(val) 
#     '''Known values for each transition in question for both Rb85 and Rb87.'''
#     Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition (MHz)
#     Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump (MHz)
#     Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2) (MHz)
#     Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4) (MHz)

def frequency_percent_difference(peak_freq):
'''Ouputs frequency data percent difference corresponding to the known values of the respective peaks. With first peak at 'zero' '''
    Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition (MHz)
    Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump (MHz)
    Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2) (MHz)
    Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4) (MHz)
    while len(peak_freq) < 6: # Add zeroes to array until 'full.' 
        peak_freq.append(0)
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
    return RB87t_perc, Rb87p_perc, Rb85t_perc, Rb85_perc

def frequency_intervals(peak_freq):
'''Outputs the frequency interval between peaks. If the the input peaks are not in increasing order, the loop breaks. There are two outputs. First (interval) is in the form of a list, the second, interval_col is the same data as a dataframe column.'''
    interval = []      
    for i in range(1, 6):
        k = peak_freq[i]-peak_freq[i-1]
        if k<0:
            print('Cursor interval c[%f]-c[%f-1] is not in increasing order.'%(i,i)) 
            break
        else:
            interval.append(k)
    interval_col = pd.DataFrame({'Intervals': interval})

def interval_percent_difference(interval):
'''Outputs the data intervals between peaks percent difference with respect to the known data values.'''
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

def error_val(raw_coords,df,q):
    #q is 10MHz conversion for trap transition, in units of voltage.
    error = df.at[raw_coords[0][0],'Error']
    error_trap = df.at[raw_coords[0][0],'Error'] - q  # q from fabry perot conversion function

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
    sns.heatmap(percentile_list, cmap = 'ocean', annot = True)
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
    sns.heatmap(percentile_list2, cmap = 'ocean', annot = True)
    plt.show()



#############
'''Alternative Functions. Combines aspects of previous functions into one.'''
'''
def percent_difference(raw_coords,conv,df): ### Need to add dataframe for EACH run, INTO the function
    # input(raw) values to voltage values
    # Outputs Percent difference between data peak values and known values(voltage)
    coords = []            # raw_coords -> coords
    for i in raw_coords:
        r = df.at[i[0],'Voltage']
        coords.append(r)
    c = []      # x-axis difference before conversion
    for i in coords:
        j = i - coords[0]
        c.append(j)
    # Difference after conversion (MHz/V)
    peak_freq = []      # Voltage of peaks with first peak at 'zero'
    for i in c:
         dd = i*conv
         peak_freq.append(dd)
    # Known Values
    Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition
    Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump
    Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2)
    Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4)

    while len(peak_freq) < 6: # Add zeroes to array until 'full'
        peak_freq.append(0)
    
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

def Intervals(peak_freq):   # Outputs voltage interval between peaks and percent difference between interval from data and known value intervals.
    # Known Values
    Rb87t = np.array([0,133.5,212,267,345.5,424])   # Rubidium 87 Trap Transition
    Rb87p = np.array([0,78.5,114.5,157,193,229])    # Rubidium 87 Pump
    Rb85t = np.array([0,60.5,92,121,152.5,184])     # Rubidium 85 (2)
    Rb85 = np.array([0,31.5,46,63,77.5,92])         # Rubidium 85 (4)
    interval = []           # Intervals
    for i in range(1, 6):
        k = peak_freq[i]-peak_freq[i-1]
        if k<0:
            print('Cursor interval c[%f]-c[%f-1] is not in increasing order.'%(i,i)) 
            break
        else:
            interval.append(k)
    interval_col = pd.DataFrame({'Intervals': interval})
    print(interval_col)

    # Interval Change in MHz (Percent Difference)
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
'''