# -*- coding: utf-8 -*-
import sys, os, posix
from se3Utils import *
try:
    sys.path.append('/etc/se3/python/')
    from  logoncfg import *
except: pass

class se3Reg:

    def __init__ (self, path2BatFiles, computer):
        """
            Open vbs registry rules, some initializations
        """
        try:
            self.__vbs = open ("%s/%s.vbs" % (path2BatFiles, computer), 'w')
            self.__computer = computer
            self.__vbsContent = []

            # Add some helpers
            if os.access ("/etc/se3/python/logonReg.vbs", os.F_OK):
                file = open ("/etc/se3/python/logonReg.vbs")
                for line in file.xreadlines ():
                    self.__vbsContent.append (line)

            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\AppData\", \"K:\profil\\appdata\", \"REG_EXPAND_SZ\"\r\n")
            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Desktop\", \"K:\profil\Bureau\", \"REG_EXPAND_SZ\"\r\n")
            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Personal\", \"K:\Docs\", \"REG_EXPAND_SZ\"\r\n")
            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Programs\", \"K:\profil\Demarrer\Programmes\", \"REG_EXPAND_SZ\"\r\n")
            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Start Menu\", \"K:\profil\Demarrer\", \"REG_EXPAND_SZ\"\r\n")
            self.__vbsContent.append ("oWsh.RegWrite \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Startup\", \"K:\profil\Demarrer\Programmes\Démarrage\", \"REG_EXPAND_SZ\"\r\n")
            
        except OSError:
           print "Can't write %s vbs in %s.vbs" % computer
           sys.exit (1)


    def __del__ (self):
        """
            Force some keys, write vbs, Delete some keys, close vbs
        """
        try:
            for line in self.__vbsContent:
                self.__vbs.write (line)
            self.__vbs.close ()

        except OSError:
            print "Can't write %s vbs in %s.vbs" % self.__computer


    def addRest (self, restrictions):
        """
            Add reg rules to vbs file
        """
        try:
            for rest in restrictions:
                if rest[3] != "SUPPR":
                    if rest[1] == "REG_DWORD":
                        self.__vbsContent.append ("oWsh.RegWrite \"%s\", CLng(%s), \"REG_DWORD\"\r\n" % (rest[0], rest[3]))
                    else:
                        self.__vbsContent.append ("oWsh.RegWrite \"%s\", \"%s\", \"%s\"\r\n" % (rest[0], rest[3], rest[1]))
                else:
                    self.__vbsContent.append ("oWsh.RegDelete \"%s\"\r\n" % rest[0])   
	
        except OSError:
            print "Can't write %s vbs in %s.vbs" % self.__computer
