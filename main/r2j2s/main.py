#!/usr/bin/env python3

from __future__ import print_function

import csv
import json
import sys

import paramiko
import websocket
from gps3 import gps3

import sshalt as ssh
import serialalt as alt

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

keysg = ["time", "lat", "lon"]
keysa = ["alt"]
keysr = ["Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP"]
keysi = ["s_pcid", "s_rc", "s_db", "s_lband",
         "s_State", "p_pcid", "p_rc", "p_db", "p_lband"]
keysj = ["E-UTRA band 1: 2100", "E-UTRA band 1: 900"]
keys = keysg + keysa + keysr + keysi + keysj
value = []
list_rows = [keys]
lastflag = False
# ----------------------------------------------------------

deviceName = '/dev/ttyACM0'  # ls -l /dev/tty.*
baudrateNum = 115200
timeoutNum = 3


# ----------------------------------------------------------
# GPSを取得　前の時間と違う値が出たら、routerの情報取得関数を実行

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

                value.append(alt.askone())

                cmd_result = ssh_sist()
                ssh2text_sist(cmd_result)

                cmd_result = ssh_cpca()
                ssh2text_cpca(cmd_result)

                cmd_result = ssh_cli()
                ssh2text_cli(cmd_result)

                list_rows.append(value)

                makecsv()
                sendsql()

                print(value)

                value = []


# ----------------------------------------------------------
# 　CSVに書き出し


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


# ----------------------------------------------------------
# 　sqlに送信


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

# ----------------------------------------------------------


def main():
    try:
        makesession()

    except KeyboardInterrupt:
        alt.close()
        sys.exit(0)


main()
