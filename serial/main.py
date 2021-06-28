import serial
import sys

deviceName = '/dev/tty.＊'    # ls -l /dev/tty.*
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
    calre = readSer.read()
    if calre == "O":
        print("calibration complete")
    elif calre == "N":
        print("Please check sensor")
        sys.exit(0)


def alt():
    # send give
    writeSer.write(give.encode())
    # take altitude
    altitude = readSer.read(2)
    return(altitude)


def main():
    try:
        cal()
        while True:
            print(alt())
    except KeyboardInterrupt:
        writeSer.close()
        readSer.close()
        sys.exit(0)


main()
