# -*- coding: utf-8 -*-
import sys, ldap
import ldap.modlist as modlist

class se3LDAP:

    scope = ldap.SCOPE_SUBTREE


    def __init__ (self, host, port, adminRdn, adminPw, baseDn, peopleRdn, computersRdn, \
                  groupsRdn, parcsRdn):
        """
            Connect to se3 LDAP
        """
        try:
            self.__ldap = ldap.initialize ("ldap://%s:%s" % (host, port))
            self.__ldap.simple_bind("%s,%s" % (adminRdn, baseDn), "%s" % adminPw)
            self.__baseDn = baseDn
            self.__peopleRdn = peopleRdn
            self.__computersRdn = computersRdn
            self.__parcsRdn = parcsRdn
            self.__groupsRdn = groupsRdn

        except ldap.LDAPError:
            print "Can't connect to ldap://%s:%s" % (host, port)
            sys.exit (1)


    def __del__ (self):
        """
            Close LDAP connexion
        """
        self.__ldap.unbind ()


    def getUserGroups (self, user):
        """
            Return a list of all user's groups
        """
        return self.__search (self.__groupsRdn, "(&(memberUid=%s)(objectClass=posixGroup))" % user, "cn") 


    def getComputerParcs (self, computer):
        """
            Return a list of all computer's parcs
        """
        return self.__search (self.__parcsRdn, "(&(member=cn=%s,%s,%s)(objectClass=groupOfNames))" % (computer, self.__computersRdn, self.__baseDn), "cn")


    def getSe3Master (self):
        """
            Return master server
        """
        try:
            return self.__search (self.__computersRdn, "l=maitre", "cn")[0]

        except IndexError:
            print "No master server !?!?"


    def getNtUserProfileStatus (self, user):
        """
            Return NT user profile status (lock, unlock, del)
            If status is deletion, set it to unlock
        """
        try:
            return self.__search (self.__peopleRdn, "uid=%s" % user, "l")[0]

        except IndexError:
            return "unlock"


    def getParcPrinters (self, parc):
        """
            Return a list of all parc's printers
        """
        printers = []
        dnList = self.__search (self.__parcsRdn, "(&(cn=%s)(objectClass=groupOfNames))" \
                                % parc, "member")
        defaultPrinterDnList = \
        self.__search (self.__parcsRdn, "(&(cn=%s)(objectClass=groupOfNames))" \
                                % parc, "owner")
        if len ((defaultPrinterDnList)):
            defaultPrinter = ldap.explode_dn (defaultPrinterDnList[0], 1)[0]
        else:
            defaultPrinter = ""

        for dn in dnList:
            rdnList = ldap.explode_dn (dn, 1)
            if rdnList[1] == "Printers":
                if rdnList[0] == defaultPrinter:
                    printers.insert (0, defaultPrinter)
                else:
                    printers.append (rdnList[0])
 
        return printers


    def setNtUserProfileStatus (self, user, status):
        """
            Unlock NT user profile status
        """
        ldif = []
        try:
            ldif.append ((ldap.MOD_REPLACE, "l", status))
            self.__ldap.modify_s ("uid=%s,%s,%s" % \
                                 (user, self.__peopleRdn, self.__baseDn), ldif)

        except ldap.INVALID_DN_SYNTAX:
            print "Invalide LDAP admin: %s,%s,%s" \
                   % (user, self.__peopleRdn, self.__baseDn)
        except ldap.STRONG_AUTH_REQUIRED:
            print "Can't modify profile status, bind as anonym"
        except ldap.LDAPError, error:
            print "Error while modifying %s profile status" %user


    def __search (self, dn, filter, attr):
        """
            Return a list based on filter and attr
        """
        resultList = []
        try:
            searchResult = self.__ldap.search_s (dn + "," + self.__baseDn, self.scope, \
                                                 filter, [attr])
            for topEntries in searchResult:
                for subEntries in topEntries[1][attr]:
                    resultList.append (subEntries)

            return resultList

        except: return resultList
