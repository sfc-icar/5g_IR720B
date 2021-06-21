#!/usr/bin/env python3

from __future__ import print_function

import csv
import json
import re
import sys

import paramiko
import websocket
from gps3 import gps3

# ----------------------------------------------------------
IP_ADDRESS = '192.168.1.1'
USER_NAME = 'admin'
PWD = "admin"
CMD = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-signal-strength'
CMD2 = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-lte-cphy-ca-info'
# ----------------------------------------------------------

# --nas-get-rf-band-info --nas-get-signal-strength --nas-get-lte-cphy-ca-info --nas-get-cell-location-info

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

keysg = ["time", "lat", "lon", "alt", "speed"]
keysr = ["Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP"]
keysi = ["s_pcid", "s_rc", "s_db", "s_lband", "s_State", "p_pcid", "p_rc", "p_db", "p_lband"]
keys = keysg + keysr + keysi
value = []
list_rows = [keys]
lastflag = False

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

                cmd_result = ssh_sist()
                ssh2text_sist(cmd_result)

                cmd_result = ssh_cpca()
                ssh2text_cpca(cmd_result)

                list_rows.append(value)

                makecsv()
                sendsql()

                print(value)

                value = []


def ssh_cpca():
    global IP_ADDRESS, USER_NAME, PWD, CMD2, client

    stdin, stdout, stderr = client.exec_command(CMD2)
    stdin.write('admin\n')
    stdin.flush()
    cmd_result = ''
    for line in stdout:
        cmd_result += line
    del stdin, stdout, stderr
    return cmd_result


def ssh2text_cpca(cmd_result_info):
    global value, list_rows

    def sc_info(ntext):
        global value, list_rows, sflag
        if "Physical Cell ID" in ntext:
            num = re.findall("Physical Cell ID: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "RX Channel" in ntext:
            num = re.findall("RX Channel: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "DL Bandwidth" in ntext:
            num = re.findall("DL Bandwidth: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "LTE Band" in ntext:
            num = re.findall("LTE Band: '(.*)'", ntext)
            fnum = [str(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "State" in ntext:
            num = re.findall("State: '(.*)'", ntext)
            fnum = [str(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
            sflag = False

    def pc_info(ntext):
        global value, list_rows, pflag
        if "Physical Cell ID" in ntext:
            num = re.findall("Physical Cell ID: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "RX Channel" in ntext:
            num = re.findall("RX Channel: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "DL Bandwidth" in ntext:
            num = re.findall("DL Bandwidth: '(.*)'", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "LTE Band" in ntext:
            num = re.findall("LTE Band: '(.*)'", ntext)
            fnum = [str(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
            pflag = False

    sflag = False
    pflag = False
    f = cmd_result_info.splitlines()
    for text in f:
        ntext = text.rstrip('\n')
        if pflag:
            pc_info(ntext)
        elif sflag:
            sc_info(ntext)
        elif "Secondary Cell Info" in ntext:
            sflag = True
        elif "Primary Cell Info" in ntext:
            pflag = True
        else:
            pass


def ssh2text_sist(cmd_result):
    global value, list_rows, lastflag

    def apnd_sist(ntext):
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

    tflag = False
    f = cmd_result.splitlines()
    for text in f:
        ntext = text.rstrip('\n')
        if tflag:
            apnd_sist(ntext)
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


def ssh_sist():
    global IP_ADDRESS, USER_NAME, PWD, CMD, client

    stdin, stdout, stderr = client.exec_command(CMD)
    stdin.write('admin\n')
    stdin.flush()
    cmd_result = ''
    for line in stdout:
        cmd_result += line
    del stdin, stdout, stderr
    return cmd_result


def makecsv():
    global list_rows
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


def sendsql():
    global value

    try:
        if __name__ == "__main__":
            websocket.enableTrace(False)
            ws = websocket.create_connection(
                "ws://203.178.143.13:5111")
            data = json.dumps(value)
            ws.send(data)
            ws.close()
    except:
        pass


def main():
    while True:
        try:
            global IP_ADDRESS, USER_NAME, PWD, client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(IP_ADDRESS,
                           username=USER_NAME,
                           password=PWD,
                           timeout=10.0)
            gps()
            client.close()
            del client

        except:
            pass


main()
