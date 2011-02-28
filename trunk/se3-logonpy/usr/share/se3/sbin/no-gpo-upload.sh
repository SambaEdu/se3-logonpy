#!/bin/bash

if [ -e /var/www/se3/includes/config.inc.php ]; then
    dbhost=`cat /var/www/se3/includes/config.inc.php | grep "dbhost=" | cut -d = -f 2 |cut -d \" -f 2`
    dbname=`cat /var/www/se3/includes/config.inc.php | grep "dbname=" | cut -d = -f 2 |cut -d \" -f 2`
    dbuser=`cat /var/www/se3/includes/config.inc.php | grep "dbuser=" | cut -d = -f 2 |cut -d \" -f 2`
    dbpass=`cat /var/www/se3/includes/config.inc.php | grep "dbpass=" | cut -d = -f 2 |cut -d \" -f 2`
elif [ -e /etc/SeConfig.ph ]; then
    dbhost=$(expr "$(grep mysqlServerIp /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
    dbuser=$(expr "$(grep mysqlServerUsername /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
    dbpass=$(expr "$(grep mysqlServerPw /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
    dbname=$(expr "$(grep connexionDb /etc/SeConfig.ph)" : ".*'\(.*\)'.*")
fi

BASEDN=$(mysql -N -h $dbhost $dbname -u $dbuser -p$dbpass -e "SELECT value FROM params WHERE name='ldap_base_dn'")
PARCSRDN=$(mysql -N -h $dbhost $dbname -u $dbuser -p$dbpass -e "SELECT value FROM params WHERE name='parcsRdn'")
ADMINRDN=$(mysql -N -h $dbhost $dbname -u $dbuser -p$dbpass -e "SELECT value FROM params WHERE name='adminRdn'")
ADMINPW=$(mysql -N -h $dbhost $dbname -u $dbuser -p$dbpass -e "SELECT value FROM params WHERE name='adminPw'")

# Nettoyage
find /home/netlogon/machine/ -name no-gpo-upload.lck -exec rm -f {} \;

#Mise en place
ldapsearch -xLLL -b $PARCSRDN,$BASEDN -D $ADMINRDN,$BASEDN -w $ADMINPW description=no-gpo-upload member|while read line
do  
    computer="$(expr "$line" : '.*cn=\([^,]*\).*')"
    if [ ! -z $computer ]; then
        [ -d /home/netlogon/machine/$computer ] && >/home/netlogon/machine/$computer/no-gpo-upload.lck
    fi
done 
