import re

import serial

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
cmd_check = "AT\r"
cmd_cell_info = "AT+cellinfolist\r"
cmd_csq = "AT+csq\r"
cmd_cgreg = "+AT+CGREG?\r"


def test():
    ser.write(cmd_check.encode())
    msg = ser.read(200)
    return_data = msg.strip().decode('utf-8')
    return_data = return_data.strip('\n')
    if "OK" in return_data:
        return True
    else:
        return False


class CellInfo:

    def __init__(self):
        self.msg = None
        self.mmc = None
        self.mnc = None
        self.cell_id = None
        self.earfcn_dl = None
        self.earfcn_ul = None
        self.rsrp = None
        self.rsrq = None
        self.sinr = None
        self.lte_rrc = None

    def get(self):
        ser.write(cmd_cell_info.encode())
        self.msg = ser.read(200)
        self.msg = self.msg.strip().decode('utf-8')

    def shaping(self):
        f = self.msg.splitlines()
        try:
            for text in f:
                ntext = text.rstrip('\n')
                self.change_to_class_data(ntext)
        except Exception as e:
            import traceback
            print("\nエラー情報:")
            traceback.print_exc()
            pass

    def change_to_class_data(self, ntext):
        if "MCC" in ntext:
            mmc = re.findall(r'\d+', ntext)
            mmc_list = [str(n) for n in mmc]
            self.mmc = mmc_list[0]
            self.mnc = mmc_list[1]
        elif "CELL_ID" in ntext:
            cell_id = re.findall(r'\d+', ntext)
            cell_id_list = [int(n) for n in cell_id]
            self.cell_id = cell_id_list[0]
        elif "earfcn_dl" in ntext:
            earfcn_dl = re.findall(r'\d+', ntext)
            earfcn_dl_list = [int(n) for n in earfcn_dl]
            self.earfcn_dl = earfcn_dl_list[0]
        elif "earfcn_ul" in ntext:
            earfcn_ul = re.findall('earfcn_ul:(.*)', ntext)
            earfcn_ul_list = [int(n) for n in earfcn_ul]
            self.earfcn_ul = earfcn_ul_list[0]
        elif "RSRP" in ntext:
            rsrp = re.findall('RSRP:(.*)', ntext)
            rsrp_list = [int(n) for n in rsrp]
            self.rsrp = rsrp_list[0]
        elif "RSRQ" in ntext:
            rsrq = re.findall('RSRQ:(.*)', ntext)
            rsrq_list = [int(n) for n in rsrq]
            self.rsrq = rsrq_list[0]
        elif "SINR" in ntext:
            sinr = re.findall(r'\d+', ntext)
            sinr_list = [float(n) for n in sinr]
            self.sinr = sinr_list[0]
        elif "LTE RRC" in ntext:
            lte_rrc = re.findall('LTE RRC:(.*)', ntext)
            lte_rrc_list = [str(n) for n in lte_rrc]
            self.lte_rrc = lte_rrc_list[0]


class Csq:
    def __init__(self):
        self.msg = None
        self.csq = None

    def get(self):
        ser.write(cmd_csq.encode())
        self.msg = ser.read(200)
        self.msg = self.msg.strip().decode('utf-8')

    def shaping(self):
        f = self.msg.splitlines()
        try:
            for text in f:
                ntext = text.rstrip('\n')
                self.change_to_class_data(ntext)
        except Exception as e:
            import traceback
            print("\nエラー情報:")
            traceback.print_exc()
            pass

    def change_to_class_data(self, ntext):
        if "csq:" in ntext:
            csq = re.findall(r'\d+', ntext)
            csq_list = [int(n) for n in csq]
            self.csq = csq_list


class Cgreg:
    def __init__(self):
        self.msg = None
        self.cgreg = None

    def get(self):
        ser.write(cmd_cgreg.encode())
        self.msg = ser.read(200)
        self.msg = self.msg.strip().decode('utf-8')

    def shaping(self):
        f = self.msg.splitlines()
        try:
            for text in f:
                ntext = text.rstrip('\n')
                self.change_to_class_data(ntext)
        except Exception as e:
            import traceback
            print("\nエラー情報:")
            traceback.print_exc()
            pass

    def change_to_class_data(self, ntext):
        if "CGREG:" in ntext:
            cgreg = re.findall(r'\d+', ntext)
            cgreg_list = [int(n) for n in cgreg]
            self.cgreg = cgreg_list


def get_all(data_list):
    data_list["cell_info"].get()
    data_list["csq"].get()
    data_list["cgreg"].get()
    return data_list


def shaping_all(data_list):
    data_list["cell_info"].shaping()
    data_list["csq"].shaping()
    data_list["cgreg"].shaping()
    return data_list


def print_data(data_list):
    print("cell_info---------------------------")
    print(data_list["cell_info"].mmc)
    print(data_list["cell_info"].mnc)
    print(data_list["cell_info"].cell_id)
    print(data_list["cell_info"].earfcn_dl)
    print(data_list["cell_info"].earfcn_ul)
    print(data_list["cell_info"].rsrp)
    print(data_list["cell_info"].rsrq)
    print(data_list["cell_info"].sinr)
    print(data_list["cell_info"].lte_rrc)
    print("csq---------------------------")
    print(data_list["csq"].csq)
    print("cgreg---------------------------")
    print(data_list["cgreg"].cgreg)


def get_new_data():
    data_list = {"cell_info": CellInfo(), "csq": Csq(), "cgreg": Cgreg()}
    if test():
        try:
            data_list = get_all(data_list)
            data_list = shaping_all(data_list)
        except:
            print('some cmd was not work')
        else:
            return_data = [data_list["cell_info"].mmc,
                           data_list["cell_info"].mnc, data_list["cell_info"].cell_id,
                           data_list["cell_info"].earfcn_dl, data_list["cell_info"].earfcn_ul,
                           data_list["cell_info"].rsrp, data_list["cell_info"].rsrq,
                           data_list["cell_info"].sinr, data_list["cell_info"].lte_rrc,
                           data_list["csq"].csq, data_list["cgreg"].cgreg
                           ]
            return return_data
    else:
        print("FS040U is dead")


if __name__ == '__main__':
    print(get_new_data())
