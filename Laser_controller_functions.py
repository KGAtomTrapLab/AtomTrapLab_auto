import pyvisa

rm = pyvisa.ResourceManager()
ThorLabs = rm.open_resource("")
Arroyo = rm.open_resource("")


def getID():
    pass


def turnOnLaser(LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else:
        print("Laser Controller doesn't exsist")


def turnOffLaser(LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else:
        print("Laser Controller doesn't exsist")


def setCurrent(current, LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else:
        print("Laser Controller doesn't exsist")


def setTempurature(temperature, LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else:
        print("Laser Controller doesn't exsist")


def getCurrent(LaserController):
    if LaserController.lower() == "arroyo":
        current = Arroyo.querry("LASer:LDI?")
        return current
    elif LaserController.lower() == "thor labs":
        current = ThorLabs.querry(":ILD:ACT?")
        current = current.split(" ")
        return current[1]
    else:
        print("Laser Controller doesn't exsist")


def getTemperature(LaserController):
    if LaserController.lower() == "arroyo":
        pass
    elif LaserController.lower() == "thor labs":
        pass
    else:
        print("Laser Controller doesn't exsist")


def getLaserStatus(LaserController):
    if LaserController.lower() == "arroyo":
        response = Arroyo.querry("LASer:OUTput?")
        if response == 1:
            return True
        elif response == 0:
            return False

    elif LaserController.lower() == "thor labs":
        response = ThorLabs.querry(":LASER?")
        response = response.split(" ")
        if response[1] == "OFF":
            return False
        elif response[1] =="ON":
            return True

    else:
        print("Laser Controller doesn't exsist")
