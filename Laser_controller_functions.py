import pyvisa

rm = pyvisa.ResourceManager()
ThorLabs = rm.open_resource("")
Arroyo = rm.open_resource("")

def getID():
    pass

def turnOnLaser(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def turnOffLaser(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def setCurrent(current,LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def setTempurature(temperature, LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def getCurrent(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def getTemperature(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")

def getLaserStatus(LaserController):
    if LaserController.lower() == 'arroyo':
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else: 
        print("Laser Controller doesn't exsist")




