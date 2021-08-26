import urllib.request
import json

API_URL = "https://icar-svr.sfc.wide.ad.jp/vggps/all_SNR"

def locateformatter(locate):
    data = (str(locate[0]) + "," + str(locate[1]) + "," + str(locate[2]))
    latlondata = ("<coordinates>" + data + "</coordinates>")
    return latlondata

def snrformatter(SNR):
    try:
        if SNR > 13:
            color = "Red"
        elif SNR > 12:
            color = "Yellow"
        else:
            color = "Green"
    finally:
        color = "<styleUrl>#"+color+"</styleUrl>"
        return color

def csv2kml(list_data):
    #====================================================#
    #KML_format
    f = open('format.txt', 'r')
    front = f.read()
    f.close()
    meat = ""
    last = "</Document>\n</kml>\n"
    #====================================================#
    for list_value in list_data:
        locatedata = [list_value[0],list_value[1],list_value[2]]
        SNR = list_value[3]
        latlondata = locateformatter(locatedata)
        color = snrformatter(float(SNR))
        data = "<Placemark>\n%s\n<Point>\n<altitudeMode>relativeToGround</altitudeMode>\n%s\n</Point>\n</Placemark>\n" % (color,latlondata)
        meat += data
    data = front+meat+last
    return data

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
        print("err")

def exportkml(data):
    f = open('./kml/export.kml', 'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    list_data = getdata(API_URL)
    data = csv2kml(list_data)
    exportkml(data)