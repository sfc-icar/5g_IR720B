from flask import Blueprint, request, abort, jsonify,Flask
import urllib.request
import json
import numpy as np
app = Flask(__name__)

@app.route('/test')
def test():
    alivetext="i`m not dead!!"
    return alivetext

@app.route('/ave', methods=['GET'])
def makeave(ax=None,bx=None,ay=None,by=None):
    #ax = request.args.get('ax', 0)
    #bx = request.args.get('bx', 1)
    #ay = request.args.get('ay', 0)
    #by = request.args.get('by', 1)
    ax = str(35.390168593)
    bx = str(35.390169595)
    ay = str(139.426184615)
    by = str(139.426484620)
    url=makeurl(ax,bx,ay,by)
    data=getdata(url)
    avedata=changeave(data)
    enc = json.dumps(avedata)
    return enc

def changeave(data):
    max=np.max(data, axis=0)
    min=np.min(data, axis=0)
    maxlat=(max[0])
    minlat=(min[0])
    maxlon=(max[1])
    minlon=(min[1])
    for i in data:
        if lat > i[0]:
            if lon > i[1]:
                data.append(i[2])
    return(maxlat)

def makeurl(ax,bx,ay,by):
    url="https://icar-svr.sfc.wide.ad.jp/vgrest/xyfind?ax="+ax+"&bx="+bx+"&ay="+ay+"&by="+by
    return url

def getdata(API_URL):
    data = []
    try:
        with urllib.request.urlopen(API_URL) as f:
            result = f.read().decode('utf-8')
            json_dict = json.loads(result)
        for resultone in json_dict:
            data.append([resultone["lon"], resultone["lat"], resultone["alt"],resultone["SNR"]])
        return data
    except:
        print("err : connectionERR!!!")

@app.errorhandler(400)
@app.errorhandler(404)
def error_handler(error):
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code

print(makeave())