import pyvisa
from pyvisa import constants
import time

time_change = 0.45  # sec/mA
currentResolution = 0.01
tempResolution = 1
rm = pyvisa.ResourceManager()

Arroyo = rm.open_resource("ASRL3::INSTR", baud_rate=38400, data_bits=8)
Arroyo.read_termination = "\r\n"
Arroyo.write_termination = "\r\n"

constants.VI_ASRL_STOP_ONE
constants.VI_ASRL_PAR_NONE
constants.VI_ASRL_FLOW_NONE

ThorLabs = rm.open_resource("GPIB0::10::INSTR")


def getID():
    pass


def beep(LaserController):
    if LaserController.lower() == "arroyo":
        Arroyo.write("*BEEP")
    elif LaserController.lower() == "thor labs":
        ThorLabs.query("*IDN?")
    else:
        print("Laser Controller doesn't exist")


def turnOnLaser(LaserController):
    if LaserController.lower() == "arroyo":
        Arroyo.write("LASer:OUTput 1")
    elif LaserController.lower() == "thor labs":
        ThorLabs.write(":LASER ON")
    else:
        print("Laser Controller doesn't exist")


def turnOffLaser(LaserController):
    if LaserController.lower() == "arroyo":
        Arroyo.write("LASer:OUTput 0")
    elif LaserController.lower() == "thor labs":
        ThorLabs.write(":LASER OFF")
    else:
        print("Laser Controller doesn't exist")

def turnOnTemp(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == 'thor labs':
        ThorLabs.write(":TEC ON")
    else: 
        print("Laser Controller doesn't exist")

def turnOffTemp(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == 'thor labs':
        ThorLabs.write(":TEC OFF")
    else: 
        print("Laser Controller doesn't exist")

def getTempStatus(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == 'thor labs':
        state = ThorLabs.write(":TEC?")
        state = state.split(' ')
        if state[1].rstrip() == "OFF":
            return False
        else:
            return True
    else: 
        print("Laser Controller doesn't exist")

def setCurrent(current, LaserController):
    if LaserController.lower() == "arroyo":
        actualCurrent = float(getCurrent("arroyo"))
        while actualCurrent != current:
            actualCurrent = float(getCurrent("arroyo"))
            difference = current - actualCurrent
            if difference < 0:
                LDI = actualCurrent - 10 * currentResolution
            else:
                LDI = actualCurrent + 10 * currentResolution
            Arroyo.write(f"LASer:LDI {LDI}")
            actualCurrent = float(getCurrent("arroyo"))
            time.sleep(time_change * 10 * currentResolution)

    elif LaserController.lower() == "thor labs":
        actualCurrent = float(getCurrent("thor labs"))
        while not((actualCurrent <= 0.001 * current + 0.0001*currentResolution) and (actualCurrent >= 0.001 * current - 0.0001*currentResolution)):
            actualCurrent = float(getCurrent("thor labs"))
            difference = 0.001 * current - actualCurrent
            if difference < 0:
                LDI = actualCurrent - 0.001 * currentResolution  # Convert to mA
            else:
                LDI = actualCurrent + 0.001 * currentResolution  # Convert to mA
            ThorLabs.write(f":ILD:SET {LDI}")
            actualCurrent = float(getCurrent("thor labs"))
            time.sleep(time_change * currentResolution)
    else:
        print("Laser Controller doesn't exist")

# Using the setCurrent as a model for set Temperature
def setTempurature(temperature, LaserController):
    if LaserController.lower() == "arroyo":
        actualTemp = float(getTemperature("arroyo"))
        while actualTemp != temperature:
            actualTemp = float(getTemperature("arroyo"))
            difference = temperature - actualTemp
            if difference < 0:
                LDI = actualTemp - 10 * tempResolution
            else:
                LDI = actualTemp + 10 * tempResolution
            #Arroyo.write(f"LASer:LDI {LDI}")
            actualTemp = float(getTemperature("arroyo"))
            time.sleep(time_change * 10 * tempResolution)

    elif LaserController.lower() == "thor labs":
        actualTemp = float(getTemperature("thor labs"))
        while not((actualTemp <= 0.001 * temperature + 0.0001*tempResolution) and (actualTemp >= 0.001 * temperature - 0.0001*tempResolution)):
            actualTemp = float(getTemperature("thor labs"))
            difference = 0.001 * temperature - actualTemp
            if difference < 0:
                NR3 = actualTemp -   tempResolution  # Convert to mA
            else:
                NR3 = actualTemp + tempResolution  # Convert to mA
            ThorLabs.write(f":RESI:SET {NR3}")
            actualTemp = float(getTemperature("thor labs"))
            time.sleep(time_change * tempResolution)
    else:
        print("Laser Controller doesn't exist")


def getCurrent(LaserController):
    if LaserController.lower() == "arroyo":
        current = Arroyo.query("LASer:SET:LDI?")
        return float(current)
    elif LaserController.lower() == "thor labs":
        current = ThorLabs.query(":ILD:SET?")
        current = current.split(" ")
        return float(current[1].rstrip())
    else:
        print("Laser Controller doesn't exist")


def getTemperature(LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        temp = ThorLabs.query(":RESI:ACT?")
        temp = temp.split(' ')
        return float(temp[1].rstrip())
    else:
        print("Laser Controller doesn't exist")


def getLaserStatus(LaserController):
    if LaserController.lower() == "arroyo":
        response = Arroyo.query("LASer:OUTput?")
        if response == 1:
            return True
        elif response == 0:
            return False

    elif LaserController.lower() == "thor labs":
        response = ThorLabs.query(":LASER?")
        response = response.split(" ")
        if response[1].rstrip() == "OFF":
            return False
        elif response[1].rstrip() == "ON":
            return True

    else:
        print("Laser Controller doesn't exist")


if __name__ == "__main__":
    x = getLaserStatus("arroyo")
    if not x:
        print("Pass laser off")
    setCurrent(50, "arroyo")
    c = getCurrent("arroyo")
    print(f"Laser current {c}")
    setCurrent(0, "arroyo")
    c = getCurrent("arroyo")
    print(f"Laser current {c}")
    print("Arroyo test end")
"""
    x = getLaserStatus("Thor labs")
    if not x:
        print("Pass laser off")
    turnOnLaser("thor labs")
    x = getLaserStatus("Thor labs")
    if x:
        print("Pass laser on")
    setCurrent(50, "thor labs")
    c = getCurrent("thor labs")
    print(f"Laser current {c}")
    setCurrent(0, "thor labs")
    c = getCurrent("thor labs")
    print(f"Laser current {c}")
    if c == 0:
        turnOffLaser("thor labs")
    else:
        print("Error laser not at 0mA")
    x = getLaserStatus("Thor labs")
    if not x:
        print("Pass laser off")
    print("Thor labs test end")"""

