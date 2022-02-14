import csv

data_place = "./csv/all.csv"

def locateformatter(locate):
    data = (locate[1] + "," + locate[0] + "," + locate[2])
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
    f = open('format_RSRP.txt', 'r')
    front = f.read()
    f.close()
    meat = ""
    for list_value in list_data:
        print(list_value[9])
        RSRP = list_value[9]
        locatedata = [list_value[1],list_value[2],list_value[3]]
        if locatedata[0] == "lat":
            continue
        else:
            latlondata = locateformatter(locatedata)

        if RSRP == "RSRP":
            continue
        else:
            color = rsrpformatter(float(RSRP))
        data = "<Placemark>\n%s\n<Point>\n<altitudeMode>relativeToGround</altitudeMode>\n%s\n</Point>\n</Placemark>\n" % (color,latlondata)
        meat += data
    last = "</Document>\n</kml>\n"
    data = front+meat+last
    return data

def opencsv(data):
    with open(data) as f:
        reader = csv.reader(f)
        list = [row for row in reader]
        return(list)

def exportkml(data):
    f = open('kml/RSRP.kml', 'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    list_data = opencsv(data_place)
    data = csv2kml(list_data)
    exportkml(data)
