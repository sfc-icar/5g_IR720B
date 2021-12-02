#!/usr/bin/env python3
import re
import subprocess
from subprocess import PIPE

iperfcmd = "iperf3 -c 203.178.143.13 -t 5"
pingcmd = "ping -c 5 203.178.143.13"


class NetworkQualityFactors:
    def __init__(self):
        self.iperf_data = None
        self.ping_data = None
        self.iperf_result = None
        self.ping_result = None

    def set_data(self):
        self.iperf_data = subprocess.Popen(iperfcmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        self.ping_data = subprocess.Popen(pingcmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    def get_data(self):
        self.iperf_result = self.iperf_data.communicate()
        self.ping_result = self.ping_data.communicate()

    def make(self):
        self.set_data()
        self.get_data()


class Iperf3Factors:
    def __init__(self):
        self.sender_transfer = None
        self.sender_bitrate = None
        self.receiver_transfer = None
        self.receiver_bitrate = None

    def shaping_iperf_data(self, listtext):
        text = listtext[0]
        ntext = text.rstrip('\n')
        sender_data = re.findall("sec  (.*)                  sender", ntext)
        sender_transfer_data = re.findall("(.*) MBytes", sender_data[0])
        self.sender_transfer = sender_transfer_data[0]
        sender_bitrate_data = re.findall("MBytes  (.*) Mbits/sec", sender_data[0])
        self.sender_bitrate = sender_bitrate_data[0]
        receiver_data = re.findall("sec  (.*)                  receiver", ntext)
        receiver_transfer_data = re.findall("(.*) MBytes", receiver_data[0])
        self.receiver_transfer = receiver_transfer_data[0]
        receiver_bitrate_data = re.findall("MBytes  (.*) Mbits/sec", receiver_data[0])
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
        self.stddev = None

    def shaping_ping_data(self, listtext):
        text = listtext[0]
        ntext = text.rstrip('\n')
        list_data = re.findall("round-trip min/avg/max/stddev = (.*) ms", ntext)
        split_data = list_data[0].split("/")
        self.min = split_data[0]
        self.avg = split_data[1]
        self.max = split_data[2]
        self.stddev = split_data[3]

    def print_test(self):
        print("ping data -------------------------")
        print("min:" + self.min)
        print("avg:" + self.avg)
        print("max:" + self.max)
        print("stddev:" + self.stddev)


def main():
    data = NetworkQualityFactors()
    data.make()
    ping_factory = PingFactors()
    iperf_factory = Iperf3Factors()
    ping_factory.shaping_ping_data(data.ping_result)
    iperf_factory.shaping_iperf_data(data.iperf_result)
    ping_factory.print_test()
    iperf_factory.print_test()


if __name__ == '__main__':
    main()
