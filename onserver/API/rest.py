from flask import Blueprint, request, abort, jsonify,Flask
import pymysql.cursors
import json
import re
app = Flask(__name__)

@app.route('/test')
def test():
    alivetext="i`m not dead"
    return alivetext


@app.route('/snr', methods=['GET'])
def snr():
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SNR FROM gndr_main"
        cursor.execute(sql)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc

@app.route('/snr/<str:xyz>', methods=['GET'])
def snrfind(xyz=None):
    num = re.findall("'(.*)'-", xyz)
    fnum = [float(n) for n in num]
    ax = fnum[0]
    num = re.findall("-'(.*)'", xyz)
    fnum = [float(n) for n in num]
    ay = fnum[0]
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SNR FROM gndr_main where %f < lat and lat < %f"
        cursor.execute(sql,ax,ay)
        result = cursor.fetchall()
    enc = json.dumps(result)
    return enc

@app.errorhandler(400)
@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
