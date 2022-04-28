#!/usr/bin/env python3
import re
import subprocess
from subprocess import PIPE

iperf_cmd_up = "iperf3 -c 203.178.143.13 -t 1 --port 50002"
iperf_cmd_down = "iperf3 -c 203.178.143.13 -t 1 -R --port 50001"
ping_cmd = "ping -c 1 icar-svr.sfc.wide.ad.jp"


class NetworkQualityFactors:
    def __init__(self):
        self.iperf_data_down = None
        self.iperf_data_up = None
        self.ping_data = None
        self.iperf_result_down = None
        self.iperf_result_up = None
        self.ping_result = None

    def set_data(self):
        self.iperf_data_up = subprocess.Popen(iperf_cmd_up, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        self.iperf_data_down = subprocess.Popen(iperf_cmd_down, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        self.ping_data = subprocess.Popen(ping_cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    def get_data(self):
        self.iperf_result_down = self.iperf_data_down.communicate()
        self.iperf_result_up = self.iperf_data_up.communicate()
        self.ping_result = self.ping_data.communicate()

    def make(self):
        self.set_data()
        self.get_data()


class Iperf3UpFactors:
    def __init__(self):
        self.sender_transfer = None
        self.sender_bitrate = None
        self.receiver_transfer = None
        self.receiver_bitrate = None

    def shaping_iperf_data(self, listtext):
        text = listtext[0]
        ntext = text.rstrip('\n')
        sender_data = re.findall("sec {2}(.*) sender", ntext)
        sender_transfer_data = re.findall("(.*) MBytes", sender_data[0])
        self.sender_transfer = sender_transfer_data[0]
        sender_bitrate_data = re.findall("MBytes {2}(.*) Mbits/sec", sender_data[0])
        self.sender_bitrate = sender_bitrate_data[0]
        receiver_data = re.findall("sec {2}(.*)receiver", ntext)
        receiver_transfer_data = re.findall("(.*) MBytes", receiver_data[0])
        self.receiver_transfer = receiver_transfer_data[0]
        receiver_bitrate_data = re.findall("MBytes {2}(.*) Mbits/sec", receiver_data[0])
        self.receiver_bitrate = receiver_bitrate_data[0]

    def print_test(self):
        print("ping iperf -------------------------")
        print("sender_transfer:" + self.sender_transfer + "MBytes")
        print("sender_bitrate:" + self.sender_bitrate + "Mbits/sec")
        print("receiver_transfer:" + self.receiver_transfer + "MBytes")
        print("receiver_bitrate:" + self.receiver_bitrate + "Mbits/sec")


class Iperf3DownFactors:
    def __init__(self):
        self.sender_transfer = None
        self.sender_bitrate = None
        self.receiver_transfer = None
        self.receiver_bitrate = None

    def shaping_iperf_data(self, listtext):
        text = listtext[0]
        ntext = text.rstrip('\n')
        print(ntext)
        sender_data = re.findall("sec {2}(.*) sender", ntext)
        sender_transfer_data = re.findall("(.*) MBytes", sender_data[0])
        self.sender_transfer = sender_transfer_data[0]
        sender_bitrate_data = re.findall("MBytes {2}(.*) Mbits/sec", sender_data[0])
        self.sender_bitrate = sender_bitrate_data[0]
        receiver_data = re.findall("sec {2}(.*)receiver", ntext)
        receiver_transfer_data = re.findall("(.*) MBytes", receiver_data[0])
        self.receiver_transfer = receiver_transfer_data[0]
        receiver_bitrate_data = re.findall("MBytes {2}(.*) Mbits/sec", receiver_data[0])
        self.receiver_bitrate = receiver_bitrate_data[0]

    def print_test(self):
        print("ping iperf -------------------------")
        print("sender_transfer:" + self.sender_transfer + "MBytes")
        print("sender_bitrate:" + self.sender_bitrate + "Mbits/sec")
        print("receiver_transfer:" + self.receiver_transfer + "MBytes")
        print("receiver_bitrate:" + self.receiver_bitrate + "Mbits/sec")


class PingFactors:
    def __init__(self):
        self.min = None
        self.avg = None
        self.max = None
        self.mdev = None

    def shaping_ping_data(self, listtext):
        text = listtext[0]
        ntext = text.rstrip('\n')
        list_data = re.findall("rtt min/avg/max/mdev = (.*) ms", ntext)
        split_data = list_data[0].split("/")
        self.min = split_data[0]
        self.avg = split_data[1]
        self.max = split_data[2]
        self.mdev = split_data[3]

    def print_test(self):
        print("ping data -------------------------")
        print("min:" + self.min)
        print("avg:" + self.avg)
        print("max:" + self.max)
        print("mdev:" + self.mdev)


def main():
    data = NetworkQualityFactors()
    data.make()

    ping_factory = PingFactors()
    iperf_down_factory = Iperf3DownFactors()
    iperf_up_factory = Iperf3UpFactors()

    ping_factory.shaping_ping_data(data.ping_result)
    iperf_down_factory.shaping_iperf_data(data.iperf_result_down)
    iperf_up_factory.shaping_iperf_data(data.iperf_result_up)

    list_data = [iperf_down_factory, iperf_up_factory.sender_transfer, ping_factory.avg]
    return list_data


def test(iperf_down_factory, iperf_up_factory, ping_factory):
    iperf_down_factory.print_test()
    iperf_up_factory.print_test()
    ping_factory.print_test()


if __name__ == '__main__':
    iperf_down_factory, iperf_up_factory, ping_factory = main()
    test(iperf_down_factory, iperf_up_factory, ping_factory)
