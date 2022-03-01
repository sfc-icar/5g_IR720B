nohup iperf3 -c 118.27.19.228 -t 100 --port 50002 -u > normal.txt &
nohup iperf3 -c 118.27.19.228 -t 100 --port 50001 -u -R > reverse.txt &