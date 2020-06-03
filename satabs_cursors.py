import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd
import seaborn as sns

# Import Data
df = pd.read_csv("testScan.txt", header=None, sep='\t')
df.columns = ['Saturated Absorption','NA', 'Error', 'NaN', 'Voltage']
for i in range(3):
    df['Saturated Absorption'][i] = 0

###########################################################################
# CURSORS

# Mouse click function to store coordinates
def storeclick(event):
    global ix, iy
    ix, iy = int(round(event.xdata)), event.ydata

    print('x = %.2f, y = %.2f'%(ix, iy))

    global raw_coords
    raw_coords.append((ix, iy))

    # 6 clicks
    if len(raw_coords) == 6:
        fig.canvas.mpl_disconnect(cid)
        plt.close()
    return

y = df['Saturated Absorption']
fig = plt.figure()
ax = fig.add_subplot()
ax.plot(y)
# ax.set_xlim([-7.5,5])

raw_coords = []

# Call click function
cid = fig.canvas.mpl_connect('button_press_event', storeclick)
cursor = Cursor(ax, useblit=True, color='r', linewidth=1.7, linestyle='--')

plt.show()
###########################################################################

# Fabry Perot:
'''Takes fabry perot data, finds free spectral range and converts the fsr from voltage to MHz/V. Ouputs MHz per voltage conversion factor as well as the 10MHz conversion for trap transition tuning.'''
    # Difference = fp_data[i+1]-fp_data[i]
    # 300/Difference = conv     # 300MHz FSR, (MHz/V)
    # q = (Difference/300)*10   # 10MHz conversion for trap transition, unit: Voltage
q = .026 #example data
conv = 539.57 # Conversion from Fabry Perot (MHZ/V) - example data
print(raw_coords)
# Convert raw x-coords to voltage values
coords = []

for i in raw_coords:
    r = df.at[i[0],'Voltage']
    coords.append(r)

# x-axis difference before conversion
c = [] 
for i in coords:
    j = i - coords[0]
    c.append(j)


d = []      # Difference after conversion (MHz/V)
for i in c:
     dd = i*conv
     d.append(dd)
print(d)

# Known Values (MHz)
# Rubidium 87 Trap Transition
Rb87t = np.array([0,133.5,212,267,345.5,424])
# Rubidium 87 Pump
Rb87p = np.array([0,78.5,114.5,157,193,229])
# Rubidium 85 (2)
Rb85t = np.array([0,60.5,92,121,152.5,184])
# Rubidium 85 (4)
Rb85 = np.array([0,31.5,46,63,77.5,92])

# Add zeroes to array until 'full'
while len(d) < 6:
    d.append(0)
# % Difference from transition - Rb 87 Trap
Rb87t_perc = []
for i in range(1, 6):
    R1 = (abs(d[i]-Rb87t[i])/(Rb87t[i]))*100
    Rb87t_perc.append(R1) 

# % Difference from transition - Rb87 pump
Rb87p_perc = []
for i in range(1, 6):
    R2 = (abs(d[i]-Rb87p[i])/(Rb87p[i]))*100
    Rb87p_perc.append(R2)

# % Difference from transition - Rb85 (2)
Rb85t_perc = []
for i in range(1, 6):
    R3 = (abs(d[i]-Rb85t[i])/(Rb85t[i]))*100
    Rb85t_perc.append(R3)

# % Difference from transition - Rb85 (4)
Rb85_perc = []
for i in range(1, 6):
    R4 = (abs(d[i]-Rb85[i])/(Rb85[i]))*100
    Rb85_perc.append(R4)

# Intervals
interval = []
for i in range(1, 6):
    k = d[i]-d[i-1]
    if k<0:
        print('Peak interval of indices,(%.1f) - (%.1f) is not in increasing order.'%(i,i-1))
        break
    else:
        interval.append(k)
interval_col = pd.DataFrame({'Intervals': interval})
print(interval_col)

# Interval Change in MHz (Percent Difference)
# Rb 87 Trap
Rb87t_pint = []
for i in range(0, 5):
    R1 = (abs(interval[i]-(Rb87t[i+1]-Rb87t[i]))/(Rb87t[i+1]-Rb87t[i]))*100
    Rb87t_pint.append(R1)

# Rb87 Pump
Rb87p_pint = []
for i in range(0, 5):
    R2 = (abs(interval[i]-(Rb87p[i+1]-Rb87p[i]))/(Rb87p[i+1]-Rb87p[i]))*100
    Rb87p_pint.append(R2)

# Rb85 (2)
Rb85t_pint = []
for i in range(0, 5):
    R3 = (abs(interval[i]-(Rb85t[i+1]-Rb85t[i]))/(Rb85t[i+1]-Rb85t[i]))*100
    Rb85t_pint.append(R3)

# Rb85 (4)
Rb85_pint = []
for i in range(0, 5):
    R4 = (abs(interval[i]-(Rb85[i+1]-Rb85[i]))/(Rb85[i+1]-Rb85[i]))*100
    Rb85_pint.append(R4)

#####################################################################
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

#######################################################################
# Error Signal Value
Rb87t_sum = (Rb87t_perc)+(Rb87t_pint)
Rb87p_sum = (Rb87p_perc)+(Rb87p_pint)
Rb85t_sum = (Rb85t_perc)+(Rb85t_pint)
Rb85_sum = (Rb85_perc)+(Rb85_pint)
if Rb87t_sum<Rb87p_sum and Rb87t_sum<Rb85t_sum and Rb87t_sum<Rb85_sum:
    print("Rb87 Trap Transition")
    transition = 1
elif Rb87p_sum<Rb87t_sum and Rb87p_sum<Rb85t_sum and Rb87p_sum<Rb85_sum:
    print("Rb87 Pump Transition")
    transition = 2
elif Rb85t_sum<Rb87t_sum and Rb87p_sum<Rb87p_sum and Rb85t_sum<Rb85_sum:
    print("Rb85 TRAP Transition")
    transition = 3
elif Rb85_sum<Rb87t_sum and Rb87p_sum<Rb87p_sum and Rb85t_sum<Rb85t_sum:
    print("Rb85 Pump Transition")
    transiton = 4
else:
    print('Lowest percent difference amongst input data was not found')
#q is 10MHz conversion for trap transition, in units of voltage.
if transition == 1:
    error = df.at[raw_coords[0][0],'Error'] - q  # q from fabry perot conversion function
else:
    error = df.at[raw_coords[0][0],'Error']
print(error)