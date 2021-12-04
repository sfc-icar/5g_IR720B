#!/usr/bin/env python3

from websocket_server import WebsocketServer
import logging
import pymysql.cursors
import csv
import time
import json


class Websocket_Server():

    def __init__(self, host, port):
        self.server = WebsocketServer(port, host=host)

    def new_client(self, client, server):
        self.server.send_message_to_all("hey all, a new client has joined us")

    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):
        row = json.loads(message)
        print(row)
        conn = pymysql.connect(
            host='localhost',
            user='feles5g',
            db='5gfeles',
            charset='utf8mb4',
            password='local5g',
            cursorclass=pymysql.cursors.DictCursor)
        for num in range(len(row)):
            if row[num] == "n/a":
                row[num] = None
        with conn.cursor() as cursor:
            sql = "INSERT INTO gndr_main(time, lat, lon, alt, Current, RSSI, ECIO, IO, SINR, RSRQ, SNR, RSRP, s_pcid, s_rc, s_db, s_lband, s_State, p_pcid, p_rc, p_db, p_lband, EUTRAband2100, EUTRAband900,ping-min, ping-avg, ping-max, ping-mdev, iperf-st, iperf-sb, iperf-rt, iperf-rb) VALUES ( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s);"
            row22 = ",".join([str(_) for _ in row[22]])
            row21 = ",".join([str(_) for _ in row[21]])
            print(row21)
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5],
                           row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30]))
        conn.commit()
        conn.close()

    def run(self):
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()


def main():
    IP_ADDR = "203.178.143.13"  # IPアドレスを指定
    PORT = 5111  # ポートを指定
    ws_server = Websocket_Server(IP_ADDR, PORT)
    ws_server.run()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
