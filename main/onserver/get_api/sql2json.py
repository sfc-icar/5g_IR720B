from flask import Blueprint, request, abort, jsonify, Flask
import pymysql.cursors
import json

app = Flask(__name__)


@app.route('/test')
def test():
    alivetext = "i`m not dead!!"
    return alivetext


@app.route('/xyall', methods=['GET'])
def snrall():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SINR,RSRP FROM vg_usb_main"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc


@app.route('/xyfind', methods=['GET'])
def snrfind(ax=None, bx=None, ay=None, by=None, alt=None, height=None):
    ax = float(request.args.get('ax', 0))
    bx = float(request.args.get('bx', 1))
    ay = float(request.args.get('ay', 0))
    by = float(request.args.get('by', 1))
    alt = float(request.args.get('alt', 1))
    height = float(request.args.get('height', 20))
    a = [ax, bx, ay, by, alt, alt + height]
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SINR,RSRP FROM vg_usb_main where %s < lat and lat < %s and %s < lon and lon < %s and %s <= alt and alt <= %s;"
        cursor.execute(sql, (a[0], a[1], a[2], a[3], a[4], a[5]))
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc

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
        sql = "SELECT * FROM vg_usb_main order by time desc limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result[0])
    return enc

@app.errorhandler(400)
@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
