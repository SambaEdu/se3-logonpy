#!/bin/bash
#shares_Win95: netlogon
#action: start
#level: 11

/usr/share/se3/logonpy_Win9x/logon.py $1 $2 $4
chmod -R 755 /home/$1/profil/Demarrer
