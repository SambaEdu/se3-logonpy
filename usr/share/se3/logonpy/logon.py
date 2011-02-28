#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time
from se3DB        import *
from se3LDAP      import *
from se3Profile   import *
from se3Logon     import *
from se3Templates import *
from se3Printers  import *
from se3Utils     import *
from se3GPO import *

nbArgs = len (sys.argv)

if nbArgs != 4:
    print "Usage: logon.py user computer arch"
    sys.exit (1)

# Get cmd line args
user = sys.argv[1]
computer = sys.argv[2]
arch     = sys.argv[3]

#########################
# Get se3 configuration #
#########################
se3db = se3DB (user, arch)
rest = []
slapdIp         = se3db.getValue ("ldap_server")
slapdPort       = se3db.getValue ("ldap_port")
adminRdn        = se3db.getValue ("adminRdn")
adminPw         = se3db.getValue ("adminPw")
baseDn          = se3db.getValue ("ldap_base_dn")
peopleRdn       = se3db.getValue ("peopleRdn")
computersRdn    = se3db.getValue ("computersRdn")
parcsRdn        = se3db.getValue ("parcsRdn")
groupsRdn       = se3db.getValue ("groupsRdn")
path2BatFiles   = se3db.getValue ("path2BatFiles")
path2Templates  = se3db.getValue ("path2Templates")
xpPass          = se3db.getValue ("xppass")
urlse3		    = se3db.getValue ("urlse3")
#########################
# Get LDAP informations #
#########################
ldap = se3LDAP (slapdIp, slapdPort, adminRdn, adminPw,\
                baseDn, peopleRdn, computersRdn, groupsRdn, parcsRdn)

groups = []
parcs  = []
# Lowercase parcs/groups  
for group in ldap.getUserGroups (user):
    groups.append (group.lower ())
for parc in ldap.getComputerParcs (computer):
    parcs.append (parc.lower ())

master   = ldap.getSe3Master ()

printers = []
for parc in parcs:
    printers += ldap.getParcPrinters (parc)

profileStatus = ldap.getNtUserProfileStatus (user)
if profileStatus == "del":
    ldap.setNtUserProfileStatus (user, "unlock")

del ldap

########################
# User profile actions #
########################
profile = se3Profile (user)

if profileStatus == "del":
    remove ("/home/profiles/%s" % user)
    remove ("/home/profiles/%s.V2" % user)
elif profileStatus == "lock":
    profile.lock ()
else:
    profile.unlock ()

try:
    if os.access ("/home/%s/profil/delHive" % user, os.F_OK):
        remove ("/home/profiles/%s" % user)
        remove ("/home/profiles/%s.V2" % user)
        os.remove ("/home/%s/profil/delHive" % user)
except: pass

templates=["base"] + groups + parcs + [computer] + [user]

##########################
# Desktop and Start Menu #
##########################
template = se3Templates (path2Templates, path2BatFiles, user)

template.cleanDesktop ()
template.cleanStartMenu ()

templatesdirs = template.getTemplates ()
restgroupes = []
for dir in templatesdirs:
    for group in dir.split ('@@'):
        for templ in templates:
            if templ == group :
                test = 1
                break
            else:
                test = 0
        if test == 0 :
            break
    if test == 1 :
        restgroupes.append (dir)
        template.createDesktop ([dir])
        template.createStartMenu ([dir])

#######################
# User logon creation #
#######################
logon = se3Logon (path2BatFiles, path2Templates, user, computer, master, arch, urlse3)

logon.addReglogon ()
logon.winsAdd ()
logon.addFirefoxAutoConfig ()
logon.addgetGPOversion ()
logon.addTemplateslogon (restgroupes)
logon.addTemplateslogoff (restgroupes)

##############################
# User restrictions creation #
##############################

restrictions = se3db.getRestrictions (restgroupes)

gpo = se3GPO (path2BatFiles, user, computer, arch, master)
gpo.addRest (restrictions)
del gpo
    

##############################
# Printers installation      #
##############################
printersVBS = se3Printers (path2BatFiles, user, computer, master)
printersVBS.clean ()
printersVBS.add (printers)
del printersVBS
del se3db
del template
del parcs
del groups

sys.exit (0)
