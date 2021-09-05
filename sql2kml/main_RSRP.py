import urllib.request
import json

API_URL = "https://icar-svr.sfc.wide.ad.jp/vggps/all_kml_old"

def locateformatter(locate):
    data = (str(locate[0]) + "," + str(locate[1]) + "," + str(locate[2]))
    latlondata = ("<coordinates>" + data + "</coordinates>")
    return latlondata

def rsrpformatter(RSRP):
    try:
        if RSRP > -80:
            color = "Blue"
        elif RSRP > -90:
            color = "Green"
        elif RSRP > -100:
            color = "Yellow"
        elif RSRP > -110:
            color = "Orange"
        else:
            color = "Red"
    finally:
        color = "<styleUrl>#"+color+"</styleUrl>"
        return color

def csv2kml(list_data):
    #====================================================#
    #KML_format
    f = open('format_RSRP.txt', 'r')
    front = f.read()
    f.close()
    meat = ""
    last = "</Document>\n</kml>\n"
    #====================================================#
    for list_value in list_data:
        if list_value[0] == None or list_value[1] == None or list_value[2] == None or list_value[3] == None:
            continue
        locatedata = [list_value[0],list_value[1],list_value[2]]
        rsrp = list_value[3]
        latlondata = locateformatter(locatedata)
        color = rsrpformatter(float(rsrp))
        mestdata = "<Placemark>\n%s\n<Point>\n<altitudeMode>relativeToGround</altitudeMode>\n%s\n</Point>\n</Placemark>\n" % (color,latlondata)
        meat += mestdata
    data = front+meat+last
    return data

def getdata(API_URL):
    data = []
    try:
        with urllib.request.urlopen(API_URL) as f:
            result = f.read().decode('utf-8')
            json_dict = json.loads(result)
        for resultone in json_dict:
            data.append([resultone["lon"], resultone["lat"], resultone["alt"],resultone["RSRP"]])
        return data
    except:
        print("err : connectionERR!!!")

def exportkml(data):
    f = open('./kml/export_RSRP.kml', 'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    list_data = getdata(API_URL)
    data = csv2kml(list_data)
    exportkml(data)