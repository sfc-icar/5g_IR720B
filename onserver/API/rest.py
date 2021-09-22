from flask import Blueprint, request, abort, jsonify
import pymysql.cursors
from flask import Flask
import json
from pymongo import DESCENDING
import pymongo

# api Blueprint作成　http://host/api 以下のものはここのルールで処理される
api = Blueprint('api', __name__, url_prefix='/api')

# エンドポイント http:/host/api/zyz, GETメソッドのみ受け付ける
# routeは複数指定も可能、methodsはリストなので複数指定可能
@api.route('/xyz', methods=['GET'])
def list_user():
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

# URL中のパラメータ取得 <type:variable_name>
# type: string(default), int, float, path, uuid
# variable_name: 変数名
#@api.route('/xyz/<int:user_id>', methods=['GET'])
#def get_user(user_id=None):
#    user = User.query.filter_by(id=user_id).first()
#    return jsonify(user.to_dict())

# エラーのハンドリング errorhandler(xxx)を指定、複数指定可能
# ここでは400,404をハンドリングする
@api.errorhandler(400)
@api.errorhandler(404)
def error_handler(error):
    # error.code: HTTPステータスコード
    # error.description: abortで設定したdict型
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code
