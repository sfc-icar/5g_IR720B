nohup iperf3 -c 203.178.143.13 -t 100 --port 50002 -u --bandwidth 300M > normal.txt &
nohup iperf3 -c 203.178.143.13 -t 100 --port 50001 -u -R --bandwidth 300M > reverse.txt &