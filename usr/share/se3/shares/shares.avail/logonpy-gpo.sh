#!/bin/bash
# $Id$
#shares_WinXP: profiles
#shares_Win2K: profiles
#shares_Vista: profiles
#shares_Seven: profiles
#action: start
#level: 01

# Should be run once by machine
[ -f  /home/netlogon/$2.lck -o -f /home/netlogon/machine/$2/no-gpo-upload.lck ] && exit 0
>/home/netlogon/$2.lck

if [ -e /etc/se3/config_m.cache.sh ]; then
	. /etc/se3/config_m.cache.sh
else

	source /var/se3/Progs/install/installdll/confse3.ini
	adminse3="$(echo $compte_admin_local|sed -e 's/\r//g')"
	xppass="$(echo $password_admin_local|sed -e 's/\r//g')"
	se3ip="$(echo $ip_se3|sed -e 's/\r//g')"
	se3_domain="$(echo $domaine|sed -e 's/\r//g')"
fi

function deleteREG
{
rm -f /home/netlogon/machine/$1/user.reg
}

function createREG
{
echo -e "REGEDIT4\r\n"> /home/netlogon/machine/$2/user.reg
flag=0
for pathreg in /home/netlogon/*.reg; do
	reg=${pathreg##*/}
	if [ ! -f /home/profiles/$1/.$reg.lck ]; then
	     sed -e "/^REGEDIT/d;/^Windows Registry Editor Version 5.00/d;s/HKEY_CURRENT_USER/HKEY_USERS\\\\$sid/g" /home/netlogon/$reg >> /home/netlogon/machine/$2/user.reg
	     touch /home/profiles/$1/.$reg.lck
	     flag=1
	echo on ajoute $reg
	fi     
done
if [ "$flag" == "0" ]; then
        deleteREG $2
fi
}

function uploadGPO
{
smbclient  //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD << EOF
	mkdir System32\GroupPolicy
	mkdir System32\GroupPolicy\User
	mkdir System32\GroupPolicy\User\Scripts
	mkdir System32\GroupPolicy\User\Scripts\Logon
	mkdir System32\GroupPolicy\User\Scripts\Logoff
	mkdir System32\GroupPolicy\Machine
	mkdir System32\GroupPolicy\Machine\Scripts
	mkdir System32\GroupPolicy\Machine\Scripts\Startup
	mkdir System32\GroupPolicy\Machine\Scripts\Shutdown
	put /home/netlogon/machine/$2/user.pol System32\GroupPolicy\User\registry.pol
	put /home/netlogon/machine/$2/logon.bat System32\GroupPolicy\User\Scripts\Logon\logon.bat
	put /home/netlogon/machine/$2/logoff.bat System32\GroupPolicy\User\Scripts\Logoff\logoff.bat
	put /home/netlogon/machine/$2/machine.pol System32\GroupPolicy\Machine\registry.pol
	put /home/netlogon/machine/$2/startup.bat System32\GroupPolicy\Machine\Scripts\Startup\startup.bat
	put /home/netlogon/machine/$2/shutdown.bat System32\GroupPolicy\Machine\Scripts\Shutdown\shutdown.bat
	put /home/netlogon/machine/$2/gpt.ini System32\GroupPolicy\gpt.ini
	put /home/netlogon/scriptsU.ini System32\GroupPolicy\User\Scripts\scripts.ini
	put /home/netlogon/scriptsC.ini System32\GroupPolicy\Machine\Scripts\scripts.ini
	put /var/se3/Docs/media/fonds_ecran/$1.$ext Web\Wallpaper\se3.$ext
	put /home/netlogon/machine/$2/printers.vbs printers.vbs
EOF
	return $?
}

function setACL
{
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/registry.pol" -S "ACL:adminse3:ALLOWED/0/FULL,ACL:SYSTEM:ALLOWED/0/FULL,ACL:$se3_domain\\$1:ALLOWED/0/READ" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/scripts.ini" -S "ACL:adminse3:ALLOWED/0/FULL,ACL:SYSTEM:ALLOWED/0/FULL,ACL:$se3_domain\\$1:ALLOWED/0/READ" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/Scripts/Logon/logon.bat" -S "ACL:adminse3:ALLOWED/0/FULL,ACL:SYSTEM:ALLOWED/0/FULL,ACL:$se3_domain\\$1:ALLOWED/0/READ" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/Scripts/Logoff/logoff.bat" -S "ACL:adminse3:ALLOWED/0/FULL,ACL:SYSTEM:ALLOWED/0/FULL,ACL:$se3_domain\\$1:ALLOWED/0/READ" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/gpt.ini" -S "ACL:adminse3:ALLOWED/0/FULL,ACL:$se3_domain\\$1:ALLOWED/0/READ,ACL:SYSTEM:ALLOWED/0/FULL,ACL:administrateurs:ALLOWED/0/FULL" || return $?
	rm -f /home/netlogon/machine/$2/fallback.bat
	rm -f /home/netlogon/machine/$2/EnableGPO.bat
}

function EnableGPO # $netbiosname $arch
{
    if [ "$2" == "Vista" ]||[ "$2" == "Seven" ]
    then
    	SHARECMD="net share C\$=C: /GRANT:adminse3,FULL\rnet share ADMIN\$ /GRANT:adminse3,FULL"
    else
	    SHARECMD="net share C\$=C:\rnet share ADMIN\$"
    fi
    sed -e s/%se3ip%/"$se3ip"/g /home/netlogon/EnableGPO.bat|sed -e s/%machine%/"$1"/g|sed -e s_%sharecmd%_"$SHARECMD"_g > /home/netlogon/machine/$1/EnableGPO.bat
    echo '\\'"$se3ip"'\netlogon\cpau.exe' -wait -lwop -hide -dec -file '\\'"$se3ip"'\netlogon\machine\gpo_helper.job' > /home/netlogon/machine/$1/fallback.bat
    echo '\\'"$se3ip"'\netlogon\machine\'"$1"'\logon.bat' >>/home/netlogon/machine/$1/fallback.bat
}

[ ! -d /home/netlogon/machine/$2 ] && mkdir -p /home/netlogon/machine/$2

(
echo username=adminse3
echo password=$xppass
echo domain=$2
)>/home/netlogon/machine/$2/gpoPASSWD
chmod 700 /home/netlogon/machine/$2/gpoPASSWD
sid=$(ldapsearch -xLLL uid=$1 sambaSID | grep sambaSID | sed "s/sambaSID: //")

case $4 in 
Vista|Seven)
    ext=jpg
;;
*)
    ext=bmp
;;
esac


# Check if some connexion already alive
# If so, don't reupload GPO if owner is current login user
# Fix XP BUG (multiple connexions to profiles at logon/logoff)
# This code mail fail, sometime, when windows upload profile,
# connexion to [home] is dead! Windows SUX.
smbstatus -S 2>/dev/null|grep $2|grep $1 >/dev/null
if [ "$?" == "0" ]
then
	/usr/share/se3/sbin/tcpcheck 1 $3:139|grep "timed out" 
	if [ "$?" == "0" ]
	then
		rm -f /home/netlogon/$2.lck
		exit 1
	fi
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/Scripts/Logon/logon.bat"  2>/dev/null |grep ACL|grep $1:  >/dev/null
	if [ "$?" == "0" ]
	then
		# GPO already in place
		rm -f /home/netlogon/$2.lck
		exit 0
	fi
fi

[ ! -d "/home/$1" ] && /usr/share/se3/shares/shares.avail/mkhome.sh $1 $2 $3 $4

# Wallpaper
if [ "$(cat /etc/se3/fonds_ecran/actif.txt 2>/dev/null)" == "1" ]
then
	/usr/share/se3/sbin/mkwall.sh $1 $ext
else
	# Delete this file, don't want logonpy to activate wallpapers GPO
	rm -f /var/se3/Docs/media/fonds_ecran/$1.*
fi
# Initial registry hack for wpkg
createREG $1 $2

/usr/share/se3/logonpy/logon.py $1 $2 $4
chmod -R 755 /home/$1/profil/Demarrer

if [ ! -f /home/netlogon/machine/$2/gpt.ini ]
then
	cp -f /home/netlogon/gpt.ini /home/netlogon/machine/$2/gpt.ini
else
	GPO_VERS="$(grep Version /home/netlogon/machine/$2/gpt.ini|cut -d '=' -f2|sed -e 's/\r//g')"
	(( GPO_VERS+=1 ))
	sed -i "s/Version=.*/Version=$GPO_VERS\r/g" /home/netlogon/machine/$2/gpt.ini
fi

# Try to upload GPO
# Sometime, Windows XP isn't ready to accept connexions on ADMIN$ (just after boot)
/usr/share/se3/sbin/tcpcheck 20 $3:445

uploadGPO $1 $2 $3
if [ "$?" == "0" ]
then
	setACL $1 $2 $3
	if [ "$?" == "1" ]
	then
	    EnableGPO $2 $4
	fi
else	    
    EnableGPO $2 $4
fi
rm -f /home/netlogon/$2.lck

