import urllib.request
import json

with urllib.request.urlopen('https://icar-svr.sfc.wide.ad.jp/vggps/all_SNR') as f:
    result = f.read().decode('utf-8')
    json_dict = json.loads(result)

for resultone in json_dict:
    location = [resultone["lat"],resultone["lon"],resultone["alt"]]
    SNR = resultone["SNR"]
    print(location,SNR)