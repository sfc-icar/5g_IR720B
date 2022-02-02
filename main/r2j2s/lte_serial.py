import serial

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=5)
cmd_check = "AT\r"
cmd_cell_info = "AT+cellinfolist\r"
cmd_csq = "AT+csq\r"


def get_check():
    ser.write(cmd_check.encode())
    msg = ser.read(64)
    print(msg.strip().decode('utf-8'))
    print('----------------\n')


def get_cell_info():
    ser.write(cmd_cell_info.encode())
    msg = ser.read(64)
    print(msg.strip().decode('utf-8'))
    print('----------------\n')



def get_csq():
    ser.write(cmd_csq.encode())
    msg = ser.read(64)
    print(msg.strip().decode('utf-8'))
    print('----------------\n')


if __name__ == '__main__':
    get_check()
    get_cell_info()
    get_csq()
