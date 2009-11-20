#!/bin/bash
#shares_WinXP: profiles
#shares_Win2K: profiles
#shares_Vista: profiles
#action: start
#level: 02
while read line
do
    echo $line|grep ">" >/dev/null
    if [ "$?" == "0" ]; then
        line="$(echo $line|sed -e 's/>//g')"
        rm -fr /home/profiles/"$1/$line"*
    else
    	rm -fr /home/profiles/"$1/$line"
    fi
done < /etc/se3/blacklist
