def gps():
    global value, keys, list_rows, key_gps
    old_data = []
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV["time"] != old_data:
                for key in key_gps:
                    data_stream.unpack(new_data)
                    value.append(data_stream.TPV[key])
                old_data = data_stream.TPV["time"]