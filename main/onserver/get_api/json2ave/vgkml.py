import json
import os
import urllib.request

import numpy as np
from flask import make_response, request, Flask

app = Flask(__name__)

width = 0.0005


def locateformatter(locate):
    data = (str(locate[0]) + "," + str(locate[1]) + "," + str(locate[2]))
    latlondata = ("<coordinates>" + data + "</coordinates>")
    return latlondata


def snrformatter(SNR):
    try:
        if SNR > 10:
            color = "Blue"
        elif SNR > 5:
            color = "Green"
        elif SNR > 0:
            color = "Yellow"
        elif SNR > -5:
            color = "Orange"
        else:
            color = "Red"
    finally:
        color = "<styleUrl>#" + color + "</styleUrl>"
        return color


def json2kml(list_data, state):
    # ====================================================#
    # KML_format
    # f = open('/var/www/html/flask/vgave/json2ave/format_SNR.txt', 'r')
    if state == "SNR":
        f = open('format_SNR.txt', 'r')
    elif state == "RSRP":
        f = open('format_RSRP.txt', 'r')
    else:
        pass
    front = f.read()
    f.close()
    meat = ""
    last = "</Document>\n</kml>\n"
    # ====================================================#
    for list_value in list_data:
        if list_value[0] is None or list_value[1] is None or list_value[2] is None or list_value[3] is None:
            continue
        locatedata = [list_value[0], list_value[1], list_value[2]]
        SNR = list_value[3]
        latlondata = locateformatter(locatedata)
        color = snrformatter(float(SNR))
        mestdata = "<Placemark>\n%s\n<Point>\n<altitudeMode>relativeToGround</altitudeMode>\n%s\n</Point>\n</Placemark>\n" % (
            color, latlondata)
        meat += mestdata
    data = front + meat + last
    return data


def changeave(data):
    ave1ddata = []
    avesnr = []
    for i in data:
        avesnr.append(i[3])
    ave1ddata.append(np.mean(avesnr, axis=0))
    return ave1ddata


def getdata(API_URL, state):
    data = []
    try:
        with urllib.request.urlopen(API_URL) as f:
            result = f.read().decode('utf-8')
            json_dict = json.loads(result)
        if state == "SNR":
            for resultone in json_dict:
                data.append([resultone["lon"], resultone["lat"], resultone["alt"], resultone["SNR"]])
        elif state == "RSRP":
            for resultone in json_dict:
                data.append([resultone["lon"], resultone["lat"], resultone["alt"], resultone["RSRP"]])
        return data
    except:
        print("err : connectionERR!!!")
        return 0


def download(procedata):
    response = make_response()
    response.data = procedata
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=snr.kml'
    return response


def makeurl(ax, bx, ay, by, alt, height):
    url = "https://icar-svr.sfc.wide.ad.jp/vgrest/xyfind?ax=" + str(ax) + "&bx=" + str(bx) + "&ay=" + str(
        ay) + "&by=" + str(by) + "&alt=" + str(alt) + "&height=" + str(height)
    return url


def get(ax, ay, bx, by, height, state):
    ax = float(ax)
    ay = float(ay)
    bx = float(bx)
    by = float(by)
    height = float(height)
    startx = ax
    starty = ay
    xlist = []
    ylist = []
    avedata = []
    alt = 0
    count = 0
    while startx < bx:
        startx += width
        xlist.append(startx)
    while starty < by:
        starty += width
        ylist.append(starty)
    print(len(xlist))
    while alt < 150:
        for x in xlist:
            for y in ylist:
                url = makeurl(x - width, x, y - width, y, alt, height)
                data = getdata(url, state)
                if data:
                    oneavelist = [y - width, x - width, alt]
                    oneavelist[len(oneavelist):len(oneavelist)] = changeave(data)
                    avedata.append(oneavelist)
                    oneavelist = []
            count += 1
            print(count)
        alt += height
    print(avedata)
    return avedata


@app.route('/test')
def test(state=None):
    state = request.args.get('state', "None")
    enc = json.dumps(state)
    return enc


@app.route('/ave', methods=['GET'])
def makeave(ax=None, ay=None, bx=None, by=None, height=None, state=None):
    ax = request.args.get('ax', 0)
    ay = request.args.get('ay', 0)
    bx = request.args.get('bx', 1)
    by = request.args.get('by', 1)
    height = request.args.get('height', 20)
    state = request.args.get('state', "None")
    avedata = get(ax, ay, bx, by, height, state)
    procedata = json2kml(avedata, state)
    enc = download(procedata)
    return enc


if __name__ == "__main__":
    port = os.getenv("PORT")
    # port = 5432
    app.run(host="0.0.0.0", port=port)
