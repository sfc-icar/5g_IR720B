import pymysql.cursors
from flask import Flask
import json
from pymongo import DESCENDING
import pymongo

app = Flask(__name__)


@app.route('/one')
def one():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main order by time desc limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result[0])
    return enc


@app.route('/ten')
def ten():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main order by time desc limit 10"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all')
def all():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_0')
def all_0():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main WHERE alt < 51"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_50')
def all_50():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main WHERE alt < 101 AND alt > 50"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_100')
def all_100():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr_main WHERE alt > 100"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_wip')
def all_wip():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT * FROM gndr"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_kml')
def all_SNR():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SNR,RSRP FROM gndr_main"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/all_kml_old')
def all_SNR_old():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SNR,RSRP FROM gndr"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc
