from flask import Blueprint, request, abort, jsonify,Flask
import urllib.request
import json
import numpy as np
app = Flask(__name__)

width=0.00001

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
    bx = str(35.390469595)
    ay = str(139.426184615)
    by = str(139.426585620)
    url=makeurl(ax,bx,ay,by)
    data=getdata(url)
    avedata=changeave(data)
    enc = json.dumps(avedata)
    return enc

def changeave(data):
    ave1ddata=[]
    ave2ddata=[]
    avelist=[]
    sorted_data=makesorteddata(data)
    lat=sorted_data[0][0]
    lon=sorted_data[0][1]
    maxlat=sorted_data[-1][0]
    maxlon=sorted_data[-1][1]
    for i in sorted_data:
        if lat >= i[0]:
            if lon >= i[1]:
                avelist.append(i[2])
            else:
                ave1ddata.append(lat)
                ave1ddata.append(lon)
                ave1ddata.append(np.mean(avelist, axis=0))
                ave2ddata.append(ave1ddata)
                ave1ddata=[]
                lon=lon+width
        else:
            lat=lat+width
    return(ave2ddata)

def makesorteddata(data):
    sorted_data = sorted(data, key=lambda x:(x[0], x[1]))
    return sorted_data

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
