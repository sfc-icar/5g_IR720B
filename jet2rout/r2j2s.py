from gps3 import gps3
import numpy as np
import paramiko
import re

# ----------------------------------------------------------
IP_ADDRESS = '192.168.1.1'
USER_NAME = 'admin'
PWD = "admin"
CMD = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-signal-strength'
# ----------------------------------------------------------

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

keys = ["time", "lat", "lon", "alt", "speed"]
value = []
list_rows = [keys]

keysr = ["Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP"]
valuer = []
list_rowsr = [keysr]
lastflag = False


def ssh():
    global IP_ADDRESS, USER_NAME, PWD, CMD

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP_ADDRESS,
                   username=USER_NAME,
                   password=PWD,
                   timeout=10.0)

    stdin, stdout, stderr = client.exec_command(CMD)

    stdin.write('admin\n')
    stdin.flush()

    cmd_result = ''
    for line in stdout:
        cmd_result += line

    client.close()
    del client, stdin, stdout, stderr
    return cmd_result


def apnd(ntext):
    global valuer, No, list_rowsr, lastflag
    print("inside apnd")
    if lastflag:
        num = re.findall("Network 'lte': '(.*) dBm", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        valuer.append(lnum)
        print("last")
        list_rowsr.append(valuer)
        valuer = []
        lastflag = False
    elif "dBm" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dBm", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        valuer.append(lnum)
    elif "dB" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dB", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        valuer.append(lnum)


def ssh2text(cmd_result):
    global valuer, No, list_rowsr, lastflag
    print("inside ssh2text")
    tflag = False
    keyflag = True
    f = cmd_result.splitlines()
    for text in f:
        ntext = text.rstrip('\n')
        if tflag:
            apnd(ntext)
            tflag = False
        elif "ECIO" in ntext:
            tflag = True
        elif "IO" in ntext:
            num = re.findall("IO: '(.*) dBm", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            valuer.append(lnum)
        elif "SINR (8)" in ntext:
            num = re.findall(": '(.*) dB", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            valuer.append(lnum)
        elif "RSRP" in ntext:
            tflag = True
            lastflag = True
        else:
            for key in keysr:
                if key in ntext:
                    tflag = True


def gps():
    global value, keys, list_rowsr
    for new_data in gps_socket:
        if new_data:
            for key in keys:
                data_stream.unpack(new_data)
                value.append(data_stream.TPV[key])
            list_rows.append(value)
            value = []
            cmd_result = ssh()
            ssh2text(cmd_result)
            np.savetxt("gps.csv", list_rows, delimiter=",", fmt='% s')
            np.savetxt("router.csv", list_rowsr, delimiter=",", fmt='% s')


def main():
    gps()


main()
