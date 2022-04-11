import serial
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


if __name__ == '__main__':

    try:
        ser = serial.Serial('/dev/tty.usbmodem1101')
        print(ser.name)

    except serial.SerialException as serial_exception:
        print(serial_exception)

        if ser.read() == b'R':
            print('read success')
            if ser.write(b'b'): print('write success')
            else: print('write failure')
        else: print('read failed')

    
    serial

    x_len = 10000 # number of points to display
    y_range = [0, 0.7] # yange of possible Y values to display

    # create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = np.linspace(0, 20, 1000)
    ys = list(np.zeros(1000))
    ax.set_ylim(y_range)

    # create a blank line. We will update the line in animate
    line, = ax.plot(xs, ys)

    # add labels
    plt.xlabel('Ramp Voltage (V)')
    plt.ylabel('Photodiode Voltage (V)')

    def response(x):
        return y_range[1]*np.exp(-(x-10)**2/(2*3**2))/2

    # this function is called periodically from FuncAnimation
    def animate(i, ys):

        y = round(np.random.uniform(0.9, 1.1)*response(xs[i*5 % x_len])+np.random.uniform(0,0.05), 2)
        # print(f'{y:.3}n')

        ys[i % x_len] = y
        # ys.append(y) # add y to list

        # ys = ys[i%x_len] # limit y list to set number of items

        line.set_ydata(ys) # update line with new Y values

        return line,

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=50, blit=True)
    plt.show()
