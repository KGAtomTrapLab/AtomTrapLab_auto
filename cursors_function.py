# Store Mouseclick Function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

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

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(y)
# ax.set_xlim([-7.5,5])

raw_coords = []

# Call click function
cid = fig.canvas.mpl_connect('button_press_event', storeclick)
cursor = Cursor(ax, useblit=True, color='r', linewidth=1.7, linestyle='--')

plt.show()