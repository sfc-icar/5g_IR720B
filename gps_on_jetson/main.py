from gps3 import gps3
import numpy as np

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

keys = ["time", "lat", "lon", "alt", "speed"]
value = []
list_rows = [keys]
count = 0

def main():
    global value, keys
    for new_data in gps_socket:
        if new_data:
            for key in keys:
                data_stream.unpack(new_data)
                value.append(data_stream.TPV[key])
            list_rows.append(value)
            value = []
            np.savetxt("out.csv", list_rows, delimiter=",", fmt='% s')

main()
