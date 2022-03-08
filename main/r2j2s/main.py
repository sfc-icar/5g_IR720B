#!/usr/bin/env python3

from __future__ import print_function

import asyncio
import csv
import json
import lte_serial as lte_ser
import serialalt as alt
import sys
import websockets
from gps3 import gps3

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

key_gps = ["time", "lat", "lon"]
key_alt = ["alt"]
key_lte = ["MCC", "MNC", "CELL_ID", "earfcn_dl", "earfcn_ul", "RSRP", "RSRQ", "SINR", "LTE RRC", "csq", "cgreg"]
keys = key_gps + key_alt + key_lte
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
    global value, keys, list_rows, key_gps
    old_data = []
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV["time"] != old_data:
                for key in key_gps:
                    data_stream.unpack(new_data)
                    value.append(data_stream.TPV[key])
                old_data = data_stream.TPV["time"]

                value.append(alt.askone())

                value = value + lte_ser.get_new_data()

                list_rows.append(value)

                makecsv()
                asyncio.run(sendsql())

                print(value)

                value = []

# ----------------------------------------------------------
# 　CSVに書き出し


def makecsv():
    global list_rows
    args = sys.argv
    try:
        csvname = "./data/" + args[1] + ".csv"
    except:
        csvname = "./data/all.csv"

    with open(csvname, "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        if isinstance(list_rows[0], list):
            writer.writerows(list_rows)
        else:
            writer.writerow(list_rows)


# ----------------------------------------------------------
# 　sqlに送信


async def sendsql():
    global value
    try:
        uri = "ws://icar-svr.sfc.wide.ad.jp:5111"
        async with websockets.connect(uri) as websocket:
            data = json.dumps(value)
            await websocket.send(data)
    except Exception as e:
        print(e)
        pass


# ----------------------------------------------------------


def main():
    try:
        alt.make()
        gps()

    except KeyboardInterrupt:
        alt.close()
        sys.exit(0)

    # except:
    # main()


main()
