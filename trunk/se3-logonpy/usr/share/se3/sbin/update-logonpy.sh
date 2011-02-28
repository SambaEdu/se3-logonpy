#!/bin/bash

# Recup param mysql
dbhost=$(expr "$(grep mysqlServerIp /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
dbuser=$(expr "$(grep mysqlServerUsername /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
dbpass=$(expr "$(grep mysqlServerPw /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
dbname=$(expr "$(grep connexionDb /etc/SeConfig.ph)" : ".*'\(.*\)'.*")

# La conf de logonpy est stocke la
echo "dbhost=\"$dbhost\"" > /etc/se3/python/mysqlinfo.py
echo "dbuser=\"$dbuser\"" >> /etc/se3/python/mysqlinfo.py
echo "dbpass=\"$dbpass\"" >> /etc/se3/python/mysqlinfo.py
echo "dbname=\"$dbname\"" >> /etc/se3/python/mysqlinfo.py


workgroup="$(grep "workgroup" /etc/samba/smb.conf|cut -d '=' -f2|sed -s "s/ //g")"
netbios="$(grep "netbios name" /etc/samba/smb.conf|cut -d '=' -f2|sed -s "s/ //g")"

# Mise en place helper cpau
if [ -e /usr/share/se3/includes/config.inc.sh ];then
. /usr/share/se3/includes/config.inc.sh -m
else
source /var/se3/Progs/install/installdll/confse3.ini
#adminse3="$(echo $compte_admin_local|sed -s 's/\r//g')"
xppass="$(echo "$password_admin_local"|sed -s 's/\r//g')"

fi

adminse3="adminse3"

/usr/share/se3/sbin/update-share.sh -a netlogon logonpy.sh Win95
/usr/share/se3/sbin/update-share.sh -a profiles logonpy-gpo.sh Win2K WinXP Vista

############################
# Fix for wine when running from sudo
export HOME=/root
############################
cd /tmp
env WINEDEBUG=-all wine /home/netlogon/CPAU.exe -u "$adminse3" -wait  -p "$xppass" -file gpo_helper.job -lwop -hide -ex "\\\\$netbios\\netlogon\\machine\\{%{COMPUTERNAME}%}\\EnableGPO.bat" -enc 
env WINEDEBUG=-all wine /home/netlogon/CPAU.exe -u "$adminse3" -wait  -p "$xppass" -file Reg_helper.job -lwop -hide -ex "regedit.exe /s \\\\$netbios\\netlogon\\machine\\{%{COMPUTERNAME}%}\\user.reg&del /q \\\\$netbios\\netlogon\\machine\\{%{COMPUTERNAME}%}\\user.reg" -enc 
rm -fr /home/netlogon/machine  && mkdir /home/netlogon/machine
mv -f gpo_helper.job /home/netlogon/machine
mv -f Reg_helper.job /home/netlogon/machine
# on efface les verrous logonpy au cas où ...
rm -f /home/netlogon/*.lck
cd - >/dev/null 2>&1
