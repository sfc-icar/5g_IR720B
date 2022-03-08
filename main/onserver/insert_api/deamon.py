#!/usr/bin/env python3

import json
import time

import pymysql.cursors

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
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
            sql = "INSERT INTO vg_usb_main(time, lat, lon, alt, MMC, MNC, cell_id, earfcn_dl, earfcn_ul, RSRP, RSRQ, SINR, LTE_RRC, csq, cgreg) VALUES ( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s);"
            cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5],
                                 row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
        conn.commit()
        conn.close()

async def main():
    async with websockets.serve(echo, "203.178.143.13", 5111):
        await asyncio.Future()  # run forever

asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
