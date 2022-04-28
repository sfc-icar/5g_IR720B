#!/usr/bin/env python3

# import asyncio
import csv
import json
import sys

import lte_serial as lte_ser
import networkalt as network
import serialalt as alt
import websockets
from gps3 import gps3

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

key_gps = ["time", "lat", "lon"]
key_alt = ["alt"]
key_lte = ["MCC", "MNC", "CELL_ID", "earfcn_dl", "earfcn_ul", "RSRP", "RSRQ", "SINR", "LTE RRC", "csq", "cgreg"]
key_net = ["up", "down", "png"]
keys = key_gps + key_alt + key_lte + key_net
value = []
list_rows = [keys]

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
            data_stream.unpack(new_data)
            make_data()
            old_data = data_stream.TPV["time"]


def make_data():
    global value
    iperf_down_factory, iperf_up_factory, ping_factory = network.main()
    network_list_data = [iperf_down_factory.sender_transfer, iperf_up_factory.sender_transfer, ping_factory.avg]
    value = [data_stream.TPV["time"], data_stream.TPV["lat"], data_stream.TPV["lon"],
             alt.askone()] + lte_ser.get_new_data() + network_list_data
    list_rows.append(value)
    make_csv()
    # asyncio.run(send_sql())
    print(value)
    value = []


# ----------------------------------------------------------
# 　CSVに書き出し


def make_csv():
    global list_rows
    args = sys.argv
    if len(sys.argv) == 1:
        csv_name = "./data/" + args[1] + ".csv"
    else:
        csv_name = "./data/all.csv"

    with open(csv_name, "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        if isinstance(list_rows[0], list):
            writer.writerows(list_rows)
        else:
            writer.writerow(list_rows)


# ----------------------------------------------------------
# 　sqlに送信


async def send_sql():
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


main()
