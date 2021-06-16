#!/usr/bin/env python3

from __future__ import print_function
from gps3 import gps3
import paramiko
import re
import websocket
import csv
import json
import sys
# ----------------------------------------------------------
IP_ADDRESS = '192.168.1.1'
USER_NAME = 'admin'
PWD = "admin"
CMD = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-signal-strength'
CMD2 = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-lte-cphy-ca-info'
# ----------------------------------------------------------

#--nas-get-rf-band-info --nas-get-signal-strength --nas-get-lte-cphy-ca-info --nas-get-cell-location-info

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

keys = ["time", "lat", "lon", "alt", "speed", "Current",
        "RSSI", "ECIO", "IO", "SINR", "RSRQ", "SNR", "RSRP", "PCID"]
keysg = ["time", "lat", "lon", "alt", "speed"]
keysr = ["Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP"]
keysi = ["PCID"]
value = []
list_rows = [keys]
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
    global value, list_rows, lastflag
    if lastflag:
        num = re.findall("Network 'lte': '(.*) dBm", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        value.append(lnum)
        lastflag = False
    elif "dBm" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dBm", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        value.append(lnum)
    elif "dB" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dB", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        value.append(lnum)


def ssh2text(cmd_result):
    global value, list_rows, lastflag
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
            value.append(lnum)
        elif "SINR (8)" in ntext:
            num = re.findall(": '(.*) dB", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "RSRP" in ntext:
            tflag = True
            lastflag = True
        else:
            for key in keysr:
                if key in ntext:
                    tflag = True


def ssh_info():
    global IP_ADDRESS, USER_NAME, PWD, CMD2
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP_ADDRESS,
                   username=USER_NAME,
                   password=PWD,
                   timeout=10.0)

    stdin, stdout, stderr = client.exec_command(CMD2)

    stdin.write('admin\n')
    stdin.flush()

    cmd_result_info = ''
    for line in stdout:
        cmd_result_info += line

    client.close()
    del client, stdin, stdout, stderr
    return cmd_result_info


def apnd_info(ntext):
    global value, list_rows
    if "Physical Cell ID" in ntext:
        num = re.findall("Physical Cell ID: '(.*)'", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        value.append(lnum)


def ssh2text_info(cmd_result_info):
    global value, list_rows
    tflag = False
    keyflag = True
    f = cmd_result_info.splitlines()
    for text in f:
        ntext = text.rstrip('\n')
        if tflag:
            apnd_info(ntext)
            tflag = False
        elif "Primary Cell Info" in ntext:
            tflag = True
        else:
            pass


def gps():
    global value, keys, list_rows, keysg
    old_data = []
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV["time"] != old_data:
                for key in keysg:
                    data_stream.unpack(new_data)
                    value.append(data_stream.TPV[key])

                old_data = data_stream.TPV["time"]

                cmd_result = ssh()
                ssh2text(cmd_result)

                cmd_result_info = ssh_info()
                ssh2text_info(cmd_result_info)

                list_rows.append(value)

                args = sys.argv
                try:
                    csvname = args[1] + ".csv"
                except:
                    csvname = "all.csv"

                with open(csvname, "w") as f:
                    writer = csv.writer(f, lineterminator='\n')
                    if isinstance(list_rows[0], list):
                        writer.writerows(list_rows)
                    else:
                        writer.writerow(list_rows)

                print(value)

                try:
                    if __name__ == "__main__":
                        websocket.enableTrace(False)
                        ws = websocket.create_connection(
                            "ws://hogehoge")
                        data = json.dumps(value)
                        ws.send(data)
                        ws.close()
                except:
                    pass

                value = []


def main():
    gps()


main()
