#!/bin/bash
# $Id$
#shares_WinXP: profiles
#shares_Win2K: profiles
#shares_Vista: profiles
#shares_Seven: profiles
#action: start
#level: 01


function deleteREG
{
rm -f /home/netlogon/machine/$1/user.reg
}

function createREG
{
echo -e "REGEDIT4\r\n"> /home/netlogon/machine/$2/user.reg
flag=0
sid=$(ldapsearch -xLLL uid=$1 sambaSID | grep sambaSID | sed "s/sambaSID: //")
# on cherche les cles qui doivent etre passees a chaque fois
for pathreg in /home/netlogon/*.ref; do
	reg=${pathreg##*/}
    if  [ -f "/home/netlogon/$reg" ]; then 
        sed -e "/^REGEDIT/d;/^Windows Registry Editor Version 5.00/d;s/HKEY_CURRENT_USER/HKEY_USERS\\\\$sid/g" /home/netlogon/$reg >> /home/netlogon/machine/$2/user.reg
        flag=1
        echo "on force $reg"
    fi
done
# on cherche les cles a passer une seule fois
for pathreg in /home/netlogon/*.reg; do
	reg=${pathreg##*/}
	if [ ! -f /home/profiles/$profile/.$reg.lck -o -f /home/netlogon/forcereg.txt ]; then
	     sed -e "/^REGEDIT/d;/^Windows Registry Editor Version 5.00/d;s/HKEY_CURRENT_USER/HKEY_USERS\\\\$sid/g" /home/netlogon/$reg >> /home/netlogon/machine/$2/user.reg
             touch /home/profiles/$profile/.$reg.lck
	     flag=1
	     echo "on ajoute $reg"
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
	put /home/netlogon/machine/$2/logon.cmd System32\GroupPolicy\User\Scripts\Logon\logon.cmd
	put /home/netlogon/machine/$2/logoff.cmd System32\GroupPolicy\User\Scripts\Logoff\logoff.cmd
	put /home/netlogon/machine/$2/machine.pol System32\GroupPolicy\Machine\registry.pol
	put /home/netlogon/machine/$2/startup.cmd System32\GroupPolicy\Machine\Scripts\Startup\startup.cmd
	put /home/netlogon/machine/$2/shutdown.cmd System32\GroupPolicy\Machine\Scripts\Shutdown\shutdown.cmd
	put /home/netlogon/machine/$2/gpt.ini System32\GroupPolicy\gpt.ini
	put /home/netlogon/scriptsU.ini System32\GroupPolicy\User\Scripts\scripts.ini
	put /home/netlogon/scriptsC.ini System32\GroupPolicy\Machine\Scripts\scripts.ini
	put /home/netlogon/machine/$2/printers.vbs printers.vbs
EOF
	return $?
}


function setGPOversion
{
smbclient  //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD << EOF
   get System32\GroupPolicy\gpt.ini /home/netlogon/machine/$2/gpt.ini
EOF
if [ "$?" != "0" ]; then
    return $?    
fi    
if [ ! -f /home/netlogon/machine/$machine/gpt.ini ]; then
	cp -f /home/netlogon/gpt.ini /home/netlogon/machine/$machine/gpt.ini
else
	GPO_VERS="$(grep Version /home/netlogon/machine/$machine/gpt.ini|cut -d '=' -f2|sed -e 's/\r//g')"
	if [ -z "$GPO_VERS" ]; then 
		cp -f /home/netlogon/gpt.ini /home/netlogon/machine/$machine/gpt.ini
	else	
		(( GPO_VERS+=65537 ))
		sed -i "s/Version=.*/Version=$GPO_VERS\r/g" /home/netlogon/machine/$machine/gpt.ini
	fi
    return 0
fi
}

function uploadWallpaper
{
if [  -f "/var/se3/Docs/media/fonds_ecran/$1.$ext" ]; then
    smbclient  //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD << EOF
	put /var/se3/Docs/media/fonds_ecran/$1.$ext Web\Wallpaper\\$1_se3.$ext
EOF
return $?
fi
return 0
}
function setADM
{
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/gpt.ini" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/registry.pol" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/scripts.ini" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/Logon" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/Logon/logon.cmd" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/Logoff" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/Logoff/logoff.cmd" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/Machine" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/Machine/registry.pol" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts/scripts.ini" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts/Startup" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts/Startup/startup.cmd" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts/Shutdown" -C "$2\\administrateur" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/Machine/Scripts/Shutdown/shutdown.cmd" -C "$2\\administrateur" || return $?
	
}

function setACL
{
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/registry.pol" -a "ACL:$se3_domain\\$1:ALLOWED/0/RDX" || return $?
	smbcacls //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD  "/System32/Grouppolicy/User/Scripts/scripts.ini" -a "ACL:$se3_domain\\$1:ALLOWED/0/RDX" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/Scripts/Logon/logon.cmd" -a "ACL:$se3_domain\\$1:ALLOWED/0/RDX" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/User/Scripts/Logoff/logoff.cmd" -a "ACL:$se3_domain\\$1:ALLOWED/0/RDX" || return $?
	smbcacls //"$3"/ADMIN$  -A /home/netlogon/machine/$2/gpoPASSWD "/System32/Grouppolicy/gpt.ini" -a "ACL:$se3_domain\\$1:ALLOWED/0/RDX" || return $?
	rm -f /home/netlogon/machine/$2/fallback.bat
	rm -f /home/netlogon/machine/$2/EnableGPO.bat
	return 0
}

function EnableGPO # $netbiosname $arch
{
    if [ "$2" == "Vista" ]||[ "$2" == "Seven" ]
    then
    	SHARECMD="net share C\$=C: /GRANT:adminse3,FULL\r\nnet share ADMIN\$ /GRANT:adminse3,FULL\r\n"
    else
	    SHARECMD="net share C\$=C:\r\nnet share ADMIN\$=%SystemRoot%\r\n"
    fi
    sed -e "s!%se3ip%!$se3ip!g;s!%machine%!$1!g;s!%sharecmd%!$SHARECMD!g;s!%user%!$user!g;s!%domain%!$se3_domain!g" /home/netlogon/EnableGPO.bat > /home/netlogon/machine/$1/EnableGPO.bat
    echo -e "start /wait \\\\\\\\$se3ip\\\\netlogon\\\\cpau.exe -wait -lwop -hide -dec -file \\\\\\\\$se3ip\\\\netlogon\\\\machine\\\\gpo_helper.job\r\n" > /home/netlogon/machine/$1/fallback.bat
    echo -e "call \\\\\\\\$se3ip\\\\netlogon\\\\machine\\\\$1\\\\logon.cmd\r\n" >>/home/netlogon/machine/$1/fallback.bat
    chown adminse3:admins /home/netlogon/machine/$1/*.bat
    chmod 664 /home/netlogon/machine/$1/*.bat
    
}

function mkgpopasswd #netbiosname
{
[ -f /home/netlogon/machine/$1 ] && rm -f /home/netlogon/machine/$1
[ ! -d /home/netlogon/machine/$1 ] && mkdir -p /home/netlogon/machine/$1
(
echo username=$1\\adminse3
echo password=$xppass
)>/home/netlogon/machine/$1/gpoPASSWD
chmod 600 /home/netlogon/machine/$1/gpoPASSWD
echo "" >&2
}

function erreur #"user" "machine" "mesg"
{
    echo "$3">&2
    /usr/share/se3/sbin/waitDel.sh /home/netlogon/$1.$2.lck 1 &
    exit 1
}


user=$1 
machine=$2 
ip=$3
type=$4
timecode="$(LC_ALL=c date +"%b %d %R")"

## verifications preliminaires
# on verife que le poste repond
/usr/share/se3/sbin/tcpcheck 10 $ip:139|grep -q "failed" && erreur $user $machine "attention le poste $ip ne repond pas" 


# on efface les verrous de plus de 5 minutes, y a pas de raison qu'ils soient encore la
find /home/netlogon -maxdepth 1 ! -cmin 5 -name *.$machine.lck -delete

# On ne le lance qu'une fois et pas si action domscripts en cours...
[ -f  /home/netlogon/$user.$machine.lck -o -f /home/netlogon/machine/$machine/no-gpo-upload.lck  ] && exit 0
if [ -f /home/netlogon/machine/$machine/action.bat ]; then
    rm /home/netlogon/machine/$machine/action.bat 
    exit 0
fi    

>/home/netlogon/$user.$machine.lck

# initialisation des parametres
. /etc/se3/config_m.cache.sh

# on initialise le dossier gpo sur le serveur
mkgpopasswd $machine


# detection de la version de windows
# a completer avec les differents builds depuis vista
if [ "$type" == "Vista" ]; then
   ret=$(echo quit|smbclient //"$3"/ADMIN$ -A /home/netlogon/machine/$2/gpoPASSWD 2>&1)
   if [ "$?" != "0" ]; then
       erreur $user $machine "$ret"    
   fi    
   build=$(echo $ret | sed 's/\(^.*OS=\[Windows \(Server\)*[ 0-9]\+ \(R2\)*[ a-zA-Z]\+ \([0-9]\+\).*\].*$\)/\4/g') 
   if [ "$build" -le "7601" ]; then
       ext=jpg
       profile=$user.V2
       ntuser=ntuser.dat
   elif [ "$build" -lt "14393" ]; then
       ext=jpg
       profile=$user.V5
       ntuser=NTUSER.DAT
   elif [ "$build" -lt "20000" ]; then
       ext=jpg
       profile=$user.V6
       ntuser=NTUSER.DAT
   else
       erreur $user $machine "probleme de detection de l'os build:$build pour $user sur la machine $machine d'ip $ip"
   fi
elif [ "$type" == "WinXP" ]; then 
   ext=bmp
   profile=$user
   ntuser=ntuser.dat
else
   erreur $user $machine "probleme de detection de l'os $type pour $user sur la machine $machine d'ip $ip"
fi



# On ne lance que si ntuser.dat a ete modifie 
if [ -f /home/profiles/$profile/$ntuser ]; then
	mtime=$(stat -c %Z /home/profiles/$profile/$ntuser 2>/dev/null)
else
	mtime=-1
fi
if [ ! -f /home/netlogon/machine/$machine/logon.lck ]; then
    oldmtime=0
else
    oldmtime=$(cat /home/netlogon/machine/$machine/logon.lck 2>/dev/null)
fi
if [ "$oldmtime" == "$mtime" ]; then
    # session deja ouverte ou overfill ?
    # overfill : on force l'execution au prochain coup (bof!)
    if getent group | grep overfill | grep -q $user ; then
        echo "0" > /home/netlogon/machine/$machine/logon.lck
        waitdel=60
    else
        waitdel=1
    fi        
    /usr/share/se3/sbin/waitDel.sh /home/netlogon/$user.$machine.lck $waitdel &
    rm -f /home/profiles/$profile/ntuser.pol
    exit 0           
fi
# nouvelle session
waitdel=1

# si le rappatriment du profile lors du premier logoff ne se faisait pas, on perdrait les GPO au login suivant, d ou la condition qui suit.
[ "$mtime" != "-1" ] && echo "$mtime" > /home/netlogon/machine/$machine/logon.lck


# creation du dossier profile sinon les acls ne sont pas  bonnes avec seven
# suppression du ntuser.ini  si pb acl
if [ -d /home/profiles/$profile ]; then  
    prop=`stat -c%U /home/profiles/$profile`
    if [ "$prop" != "$user" ]; then
         chown -R $user:lcs-users /home/profiles/$profile > /dev/null 2>&1
    fi
    getfacl -pc /home/profiles/$profile | grep -q "mask::"
    if [ "$?" == "0" ]; then
        setfacl -R -b /home/profiles/$profile
        chown -R $user:lcs-users /home/profile/$profile > /dev/null 2>&1
        chmod 777 /home/profiles/$profile
        chmod 600 /home/profiles/$profile/$ntuser /home/profiles/$profile/ntuser.pol
        rm -f /home/profiles/$profile/ntuser.ini
    fi
else
    mkdir -p /home/profiles/$profile
    chown  $user:lcs-users /home/profiles/$profile
fi

# Check if some connexion already alive
/usr/share/se3/sbin/tcpcheck 30 $ip:139|grep -q "failed" 
if [ "$?" == "0" ]
then
	[ ! -d "/home/$user" ] && /usr/share/se3/shares/shares.avail/mkhome.sh $user $machine $ip $type
        EnableGPO $machine $type 
	erreur $user $machine "la machine $machine ne repond pas"
fi


echo "$timecode --ouverture de session de $user sur $ret revision $build--" >&2
[ ! -d "/home/$user" ] && /usr/share/se3/shares/shares.avail/mkhome.sh $user $machine $ip $type

# Wallpaper
if [ "$(cat /etc/se3/fonds_ecran/actif.txt 2>/dev/null)" == "1" ]
then
	/usr/share/se3/sbin/mkwall.sh $user $ext
else
	# Delete this file, don't want logonpy to activate wallpapers GPO
	rm -f /var/se3/Docs/media/fonds_ecran/$user.*
fi
# Initial registry hack for wpkg
createREG $user $machine
if [ "$localmenu" == "1" ]
then
	pathDemarrer="/home/profiles/$profile/Demarrer"
#	[ ! -d "$pathDemarrer" ] && mkdir -p "$pathDemarrer" && chown -R  $user:lcs-users "/home/profiles/$profile"
else
	pathDemarrer="/home/$user/profil/Demarrer"
	chown $user:admins $pathDemarrer/Programmes
	chmod -R 755 "$pathDemarrer"
fi
/usr/share/se3/logonpy/logon.py $user $machine $type

chown -R adminse3:admins /home/netlogon/machine/$machine
chmod 755 /home/netlogon/machine/$machine
chmod 664 /home/netlogon/machine/$machine/*
chmod 600 /home/netlogon/machine/$machine/gpoPASSWD

# on verifie que les GPO SE3 sont installee sur le poste, sinon on les installe
setGPOversion $user $machine $ip && smbcacls //"$ip"/ADMIN$ -A /home/netlogon/machine/$machine/gpoPASSWD "/system32/Grouppolicy/se3.log">/dev/null 2>&1 && uploadGPO $user $machine $ip
if [ "$?" == "0" ]
then
    uploadWallpaper $user $machine $ip && setADM $user $machine $ip && setACL $user $machine $ip 
	if [ "$?" == "1" ]
	then
	    EnableGPO $machine $type
	fi
else	    
    EnableGPO $machine $type
fi
# on n'efface le lock qu'au bout de quelques secondes
/usr/share/se3/sbin/waitDel.sh /home/netlogon/$user.$machine.lck $waitdel &
echo "" >&2
