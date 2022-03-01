
https://icar-svr.sfc.wide.ad.jp/vgrest/xyfind?ax=35.390168593&bx=35.390168595&ay=139.426184615&by=139.426484620&alt=0
https://icar-svr.sfc.wide.ad.jp/vgrest/xyall
https://icar-svr.sfc.wide.ad.jp/vgrest/test

https://icar-svr.sfc.wide.ad.jp/vgkml/test?state=SNR
https://icar-svr.sfc.wide.ad.jp/vgkml/snrave?ax=35.387958&ay=139.425070&bx=35.392375&by=139.428492

http://172.20.10.2:5000/snrave?ax=35.387958&ay=139.425070&bx=35.392375&by=139.428492&state=SNR
0.0.0.0:5432/test?state=SNR

35.387958, 139.425070, 35.392375, 139.428492

ALTER TABLE gndr_main ADD (ping_min FLOAT, ping_avg FLOAT, ping_max FLOAT, ping_mdev FLOAT, iperf_st FLOAT, iperf_sb FLOAT, iperf_rt FLOAT, iperf_rb FLOAT);
