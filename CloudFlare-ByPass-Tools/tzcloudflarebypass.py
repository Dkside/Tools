#!/usr/bin/python
import socket

subdomainlist = ["ftp", "cpanel", "webmail" , "mail" , "www", "www1", "www2", "www3", "www4", "www5","ns1", "ns2" , "forums" , "blog"]

print ('\033[1m' + "CLOUDFLARE BYPASS SCRIPT ") 

host = raw_input("Web Site Giriniz : Ornek:discordapp.com = ")
for sublist in subdomainlist:
    try:
       hosts = str(sublist) + "." + str(host)
       showip = socket.gethostbyname(str(hosts))
       print " Cloudflare has begun to be bypassed  "+str(showip)+' :| '+str(hosts)
    except:
            	pass

print ( '\033[93m' + "TURKISH HACKERS GROUP")
print ( '\033[92m' + "darksecarmy.com")  
