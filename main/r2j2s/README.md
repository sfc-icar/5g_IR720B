## 動かすもの

```shell
> screen /dev/ttyACM0 115200
> sudo usb_modeswitch -c /etc/usb_modeswitch.conf
> sudo wvdial
> ip addr | grep "inet 10"
> sudo route add default gw 
> cd iperf3
> bash main.sh
> cd ..
> nohup python3 main.py 100m &
```

## 終わったら
それぞれの名前を変更