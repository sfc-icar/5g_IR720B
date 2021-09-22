from flask import Blueprint, request, abort, jsonify,Flask
import pymysql.cursors
import json
app = Flask(__name__)

@app.route('/test')
def test():
    alivetext="i`m not dead!!"
    return alivetext


@app.route('/snrall', methods=['GET'])
def snrall():
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

@app.route('/snrfind', methods=['GET'])
def snrfind(ax=None,bx=None):
    ax = float(request.args.get('ax', 0))
    bx = float(request.args.get('bx', 1))
    a=[ax,bx]
    conn = pymysql.connect(
        host='localhost',
        user='feles5g',
        db='5gfeles',
        charset='utf8mb4',
        password='local5g',
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        sql = "SELECT lat,lon,alt,SNR FROM gndr_main where %s < lat and lat < %s ;"
        cursor.execute(sql,(a[0],a[1]))
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