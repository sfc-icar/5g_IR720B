import csv

data_place = "./sample.csv"

def locateformatter(locate):
    data = (locate[0] + "," + locate[1] + "," + locate[2])
    latlondata = ("<coordinates>" + data + "</coordinates>")
    return latlondata

def snrformatter(SNR):
    if SNR > 13:
        color = "Red"
    elif SNR > 12:
        color = "Yellow"
    elif SNR > 0:
        color = "Green"
    color = "<styleUrl>#"+color+"</styleUrl>"
    print(SNR)
    print(color)
    return color

def csv2kml(list_data):
    f = open('format.txt', 'r')
    front = f.read()
    f.close()
    meat = ""
    for list_value in list_data:
        SNR = list_value[11]
        locatedata = [list_value[1],list_value[2],list_value[3]]
        latlondata = locateformatter(locatedata)

        if SNR == "SNR":
            continue
        else:
            color = snrformatter(float(SNR))
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
    f = open('export.kml', 'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    list_data = opencsv(data_place)
    data = csv2kml(list_data)
    exportkml(data)