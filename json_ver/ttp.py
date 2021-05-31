# import subprocess
import re
import json

keys = ["Current", "RSSI", "ECIO", "IO", "SINR(8)", "RSRQ", "SNR", "RSRP", "Time"]
value = []


# result = subprocess.check_output(
#    ["qmicli", "-d", "/dev/cdc-wdm1", "--nas-get-signal-strength"])

def apnd(ntext):
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

def main():
    tflag = False
    keyflag = False
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
        else:
            for key in keys:
                if key in ntext:
                    tflag = True
    f.close()


main()
data = dict(zip(keys, value))
with open('out.json', mode='wt', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
