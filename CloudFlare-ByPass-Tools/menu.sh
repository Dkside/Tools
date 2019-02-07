#!/bin/bash
BLACK='\e[0;30m'
BLUE='\e[0;34m'
GREEN='\e[0;32m'
CYAN='\e[0;36m'
RED='\e[0;31m'
PURPLE='\e[0;35m'
BROWN='\e[0;33m'
LIGHTGRAY='\e[0;37m'
DARKGRAY='\e[1;30m'
LIGHTBLUE='\e[1;34m'
LIGHTGREEN='\e[1;32m'
LIGHTCYAN='\e[1;36m'
LIGHTRED='\e[1;31m'
LIGHTPURPLE='\e[1;35m'
YELLOW='\e[1;33m'
WHITE='\e[1;37m'
NC='\e[0m'              

exit_script()
{
  echo "* * *Trap * * *"
  ./menu
}

CloudFlareByPass()
{
    clear
    echo -e " ${BLUE} "
	echo "  |-----------------------------------------------------------------------| "
    echo "  |                   @cagriii_cifcii and @yanlzkurt5757                  |  "
    echo "  |-----------------------------------------------------------------------| "
    echo -e " "
    echo -e "       ${RED}██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗"
    echo -e "       ${BLUE}██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝"
    echo -e "       ${WHITE}██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗"
    echo -e "       ${GRAY}██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║"
    echo -e "       ${BROWN}██████╔╝   ██║   ██║     ██║  ██║███████║███████║"
    echo -e "       ${PURPLE}╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝"
    echo -e "       ${CYAN}            "
    echo -e "       ${RED}		--=[CloudFlare ByPass]=--"                 
    echo -e "       ${CYAN} "
python cloulflarebypass.py
echo " Enter'a Basarak Geri Dönebilirsiniz."
read enter

}

ByPass()
{
    clear
    echo -e " ${BLUE} "
        echo "  |-----------------------------------------------------------------------| "
    echo "  |              @cagriii_cifcii and @yanlzkurt5757                       |"
    echo "  |-----------------------------------------------------------------------| "
./dnsresolver.sh

}

hatcloud()
{
    clear
    echo -e " ${WHITE} "
	echo "  +-----------------------------------------------------------------------+ "
    echo "                             @cagriii_cifcii and @yanlzkurt5757               "
    echo "  +-----------------------------------------------------------------------+ "
    echo "    ██████╗ ███████╗ █████╗ "
    echo "    ██╔══██╗██╔════╝██╔══██╗"
    echo "    ██║  ██║███████╗███████║"
    echo "    ██║  ██║╚════██║██╔══██║"
    echo "    ██████╔╝███████║██║  ██║"
    echo "    ╚═════╝ ╚══════╝╚═╝  ╚═╝"
echo "HEDEF SITE :"
read host
clear
./hatcloud.rb -b $host
echo " "
echo " Enter'a Basarak Geri Dönebilirsiniz."
read enter
}

Tzcbypass()
{
    clear
    echo -e " ${WHITE} "
	echo "  +-----------------------------------------------------------------------+ "
    echo "                             @cagriii_cifcii and @yanlzkurt5757               "
    echo "  +-----------------------------------------------------------------------+ "
    echo "		████████▄     ▄████████    ▄████████ "
    echo "		███   ▀███   ███    ███   ███    ███ "
    echo "		███    ███   ███    █▀    ███    ███ "
    echo "		███    ███   ███          ███    ███ "
    echo "		███    ███ ▀███████████ ▀███████████ "
    echo "		███    ███          ███   ███    ███ "
    echo "		███   ▄███    ▄█    ███   ███    ███ "
    echo "		████████▀   ▄████████▀    ███    █▀  "

python tzcloudflarebypass.py -b $host
echo " "
echo " Enter'a Basarak Geri Dönebilirsiniz."
read enter
}

exit_script1()
{
  exit 1
}

Take_input1()
{
clear
while :
do
clear
echo -e "${WHITE}                                                
                           " "${GREEN}DARKSECARMY.COM "${RED}BETA YAZILIMDIR
echo -e "${WHITE}
╔═╗┬  ┌─┐┬ ┬┌┬┐╔═╗┬  ┌─┐┬─┐┌─┐${RED}
║  │  │ ││ │ ││╠╣ │  ├─┤├┬┘├┤ ${PURPLE}
╚═╝┴─┘└─┘└─┘─┴┘╚  ┴─┘┴ ┴┴└─└─┘ COLAK & CAGRI CIFTCI ${WHITE}
"${WHITE}
    echo -e "${WHITE}Note: "${GREEN}CTRL + Z YAPARAK SCRIPTDEN CIKIS YAPABILIRSINIZ
    echo -e "${WHITE}[===============> DARKSECARMY.COM <==================]"
    echo -e "${LIGHTBLUE}[1]${PURPLE}CloudFlareByPass "                                               
    echo -e "${LIGHTBLUE}[2]${GREEN}ByPass${LIGHTBLUE}  "                                            
    echo -e "${LIGHTBLUE}[3]${WHITE}HatCloud${LIGHTBLUE}    "  
    echo -e "${LIGHTBLUE}[4]${RED}tzcloudflarebypass${LIGHTBLUE}    "  
    echo -n "Menuden Scriptleri Secebilirsiniz [1 - 4] "
    read yourch                                          
    case $yourch in
      1) CloudFlareByPass ;;
      2) ByPass ;;
      3) hatcloud ;;
      4) Tzcbypass ;;
      ex) echo "As you Command" ;  exit 1  ;;
      *) echo "HATALI RAKAM GIRDINIZ" ;
         echo "Enter Basarak Menuye Dönebilirsiniz . . ." ; read ;;
 esac
done # end_while
}
#
# Set trap to for CTRL+C interrupt i.e. Install our error handler
# When occurs it first it calls del_file() and then exit
#
trap exit_script 2
#
# Call our user define function : Take_input1
#
Take_input1
