import re
import numpy as np

keys = ["No", "Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP", "Time"]
value = []
list_rows = [keys]
No = 0;


def apnd(ntext):
    global value, No,list_rows
    if "dBm" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dBm", ntext)
        fnum = [float(n) for n in num]  # floatに
        lnum = fnum[0]
        value.append(lnum)
    elif "dB" in ntext and "Network" in ntext:
        num = re.findall("Network 'lte': '(.*) dB", ntext)
        fnum = [float(n) for n in num]
        lnum = fnum[0]
        value.append(lnum)
    elif "2021" in ntext:
        value.append(ntext)
        list_rows.append(value)
        value = []


def main():
    global value, No
    tflag = False
    keyflag = True
    f = open('plug.txt', 'r')
    for text in f:
        ntext = text.rstrip('\n')
        if tflag:
            apnd(ntext)
            tflag = False
        elif "ECIO" in ntext:
            tflag = True
        elif "IO" in ntext:
            num = re.findall("IO: '(.*) dBm", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "SINR (8)" in ntext:
            num = re.findall(": '(.*) dB", ntext)
            fnum = [float(n) for n in num]
            lnum = fnum[0]
            value.append(lnum)
        elif "time" in ntext:
            tflag = True
            keyflag = True
        elif "Successfully" in ntext and keyflag:
            keyflag = False
            No += 1
            value.append(No)
        else:
            for key in keys:
                if key in ntext:
                    tflag = True
    f.close()


main()
np.savetxt("out.csv", list_rows, delimiter=",", fmt='% s')
