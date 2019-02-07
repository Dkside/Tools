# wifi-ddos
练手小玩具  
`//TODO:  
自动找到网卡开启监听；
输入ssid自动找到对应MAC进行攻击（针对一个SSID多台设备）；`

## 食用方式
kali下打开网卡监听模式：  
```iwconfig```查看无线网络情况,找到设备  
```airmon-ng start iface```启用网卡监听模式  
```python wifi-ddos.py -i ifacemon -s```扫描AP  
...