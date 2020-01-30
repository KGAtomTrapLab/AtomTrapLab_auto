import Laser_controler_functions
import matplotlib
import sys
import os

"""
This program automatically tunes the pump and trap lasers from the lab
inputs: 
    - Laser Current [mA]
    - Laser Temperature [kOhms / Celcius]
    - Sweep voltage 
        -Vmax [V]
        -Vmin [V]
    - Sweep time [s]
    - Laser Controler

Outputs: 
    - Laser Controller
    - Laser Current [mA]
    - Sweep Voltages [V]
    - Sweep Time [s]
    - Thershold Current [mA]
    - Plots of 
        - Saturated Absorbtion [units]
        - Fabrey Perro 
        - Error
    - Transition match
"""


def find_threshold_current():
    pass


def set_laser_values(current, temp, laserController):
    Laser_controller_functions.setCurrent(current, laserController)
    Laser_controller_functions.setTempurature(temp, laserController)


def run_labVIEW(Vmax, Vmin, sweepTime):
    os.system(
        f"C:\\Users\\Kat\\Desktop\\builds\\Application.exe -- {Vmax} {Vmin} {sweepTime}"
    )  # Need to find actuall location


def read_csv():  # Anya's Code
    pass


def plot_graphs():  # Inputs from csv
    pass


def cursors_inputs():  # Cursers to Excel document
    pass


def read_exel():
    pass


if __name__ == "__main__":
    name, current, temp, Vmax, Vmin, sweepTime, laserControler = sys.argv

    # thresholdCurrent = find_threshold_current()
    set_laser_values(current, temp, laserControler)
    run_labVIEW(Vmax, Vmin, sweepTime)
    read_csv()
    plot_graphs()
    cursors_inputs()
    transition = read_exel()

