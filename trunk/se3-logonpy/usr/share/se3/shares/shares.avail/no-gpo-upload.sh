#!/bin/bash
#shares_WinXP: netlogon
#shares_Win2K: netlogon
#shares_Vista: netlogon
#action: start
#level: 01

[ ! -f /home/netlogon/machine/$2/no-gpo-upload.lck ] && exit 0
[ "$1" == "adminse3" ] && exit 0 # CPAU.exe

source /var/se3/Progs/install/installdll/confse3.ini
adminse3="$(echo $compte_admin_local|sed -e 's/\r//g')"
passadmin="$(echo $password_admin_local|sed -e 's/\r//g')"
se3ip="$(echo $ip_se3|sed -e 's/\r//g')"
dom="$(echo $domaine|sed -e 's/\r//g')"

/usr/share/se3/logonpy/logon.py $1 $2 $4

if [ ! -f /home/netlogon/machine/$2/gpt.ini ]
then
	cp -f /home/netlogon/gpt.ini /home/netlogon/machine/$2/gpt.ini
else
	GPO_VERS="$(grep Version /home/netlogon/machine/$2/gpt.ini|cut -d '=' -f2|sed -e 's/\r//g')"
	(( GPO_VERS+=1 ))
	sed -i "s/Version=.*/Version=$GPO_VERS\r/g" /home/netlogon/machine/$2/gpt.ini
fi

if [ "$4" == "Vista" ]
then
	SHARECMD="net share C\$=C: /GRANT:adminse3,FULL"
else
	SHARECMD="net share C\$=C:"
fi

sed -e s/%se3ip%/"$se3ip"/g /home/netlogon/EnableGPO.bat|sed -e s/%machine%/"$2"/g|sed -e s_%sharecmd%_"$SHARECMD"_g|sed s/%user%/$1/g|sed -e s/%domain%/$dom/g|sed -e s/netsh.*//g|sed -e s/.*printers.*//g > /home/netlogon/machine/$2/EnableGPO.bat
echo '\\'"$se3ip"'\netlogon\cpau.exe' -wait -lwop -hide -dec -file '\\'"$se3ip"'\netlogon\machine\gpo_helper.job' > /home/netlogon/machine/$2/fallback.bat
echo '\\'"$se3ip"'\netlogon\machine\\'"$2\logon.bat" >>/home/netlogon/machine/$2/fallback.bat
