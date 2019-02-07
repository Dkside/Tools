# -*- coding:utf-8 -*-

import sys
import os

print "\n"

print "1) Debian Ubuntu Linux Mint"

print "2) Fedora"

print "3) OpenSUSE"
print "\n"
n = input("kaosetup >")

os.system("clear")

if n == 1:
   os.system("sudo apt-get install siege")
   os.system("sudo apt-get install hping3")
   os.system("sudo apt-get install ping")
   os.system("sudo apt-get install xterm")
   os.system("cd usr")
   os.system("cd pydos")
   os.system("sudo cp pydos /usr/bin")
   os.system("sudo cp DOSAPP /usr/bin")
   os.system("cd ..")
   os.system("cd ..")
   os.system("sudo cp -Rf etc/DOS.py /etc/init.d/DOS.py")
   os.system("sudo cp -Rf pyDoS.desktop /usr/share/applications")
   os.system("sudo cp -Rf opt/pydos /opt/pydos")
   os.system("chmod +x /etc/init.d/DOS.py /usr/bin/pydos /usr/bin/DOSAPP /usr/share/applications")
  



if n == 2:
   os.system("sudo yum install siege")
   os.system("sudo yum install hping3")
   os.system("sudo yum install ping")
   os.system("sudo yum install xterm")
   os.system("cd usr")
   os.system("cd pydos")
   os.system("sudo cp pydos /usr/bin")
   os.system("sudo cp DOSAPP /usr/bin")
   os.system("cd ..")
   os.system("cd ..")
   os.system("sudo cp -Rf etc/DOS.py /etc/init.d/DOS.py")
   os.system("sudo cp -Rf pyDoS.desktop /usr/share/applications")
   os.system("sudo cp -Rf opt/pydos /opt/pydos")
   os.system("chmod +x /etc/init.d/DOS.py /usr/bin/pydos /usr/bin/DOSAPP /usr/share/applications")

if n == 3:
   os.system("sudo zypper install siege")
   os.system("sudo zypper install hping3")
   os.system("sudo zypper install ping")
   os.system("sudo zypper install xterm")
   os.system("cd usr")
   os.system("cd pydos")
   os.system("sudo cp pydos /usr/bin")
   os.system("sudo cp DOSAPP /usr/bin")
   os.system("cd ..")
   os.system("cd ..")
   os.system("sudo cp -Rf etc/DOS.py /etc/init.d/DOS.py")
   os.system("sudo cp -Rf pyDoS.desktop /usr/share/applications")
   os.system("sudo cp -Rf opt/pydos /opt/pydos")
   os.system("chmod +x /etc/init.d/DOS.py /usr/bin/pydos /usr/bin/DOSAPP /usr/share/applications")

os.system("clear")

print "! Su sistema ya está preparado ¡"
