import serial
import sys
import time

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
    altitude1 = readSer.read()
    altitude2 = readSer.read()
    altitude1 = str(int.from_bytes(altitude1, 'big'))
    altitude2 = str(int.from_bytes(altitude2, 'big'))
    altitude = int(altitude1+altitude2)
    return(altitude)


def main():
    makesession()
    try:
        cal()
        while True:
            print(alt())
            time.sleep(1)
    except KeyboardInterrupt:
        writeSer.close()
        readSer.close()
        sys.exit(0)


main()
