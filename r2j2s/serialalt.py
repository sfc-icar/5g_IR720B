import time
import sys
import serial

deviceName = '/dev/ttyACM0'    # ls -l /dev/tty.*
baudrateNum = 115200
timeoutNum = 3
calibration = "C"
give = "G"


def makesession():
    global writeSer, readSer
    # Make session
    writeSer = serial.Serial(deviceName, baudrateNum, timeout=timeoutNum)
    readSer = serial.Serial(deviceName, baudrateNum, timeout=timeoutNum)


def cal():
    # calibration
    writeSer.write(calibration.encode())
    time.sleep(5)
    calre = readSer.read()
    calre = calre.decode()
    #calre = str.from_bytes(calre, 'big')
    if calre == "O":
        print("calibration complete")
    elif calre == "N":
        print("Please check sensor")


def alt():
    # send give
    writeSer.write(give.encode())
    # take altitude
    altitude1 = readSer.read()
    altitude2 = readSer.read()
    altitude1 = str(int.from_bytes(altitude1, 'big'))
    altitude2 = str(int.from_bytes(altitude2, 'big'))
    altitude = int(altitude1+altitude2)
    return(altitude)


def make():
    makesession()
    cal()


def askone():
    return(alt())


def close():
    writeSer.close()
    readSer.close()
