# -*- coding: utf-8 -*-
import sys, os, posix
from se3Utils import *

class se3Logon:

    def __init__ (self, path2BatFiles, path2Templates, user, computer, master, arch):
        """
            Open logon bat, some initializations
        """
        try: 
            self.__logonU = open ("%s/%s.bat" % (path2BatFiles, computer), 'w')
            self.__logonU.write ("\\\\%s\\netlogon\\killexplorer.exe 0\r\n" % master)
            self.__logonU.write ("cscript \\\\%s\\netlogon\\%s.vbs\r\n" % (master, computer))
            self.__tplPath = path2Templates
            self.__user = user
            self.__computer = computer
            self.__master = master
            self.__arch = arch

        except OSError:
            print "Can't create %s/%s/.bat" % (computer, user)
            sys.exit (1)
			

    def __del__ (self):
        """
            Close logon bat
        """
        try:
            self.__logonU.write ("\\\\%s\\netlogon\\fde.exe\r\n" % self.__master)
            self.__logonU.close ()
            
        except OSError:
           print "Can't write %s/%s.bat" % (self.__user, self.__computer)


    def addTemplateslogon (self, templates):
        """
            Add templates logon, ignore se3printers.bat
        """
        try:
            for template in templates:
                if os.access ("%s/%s/logon.bat" % (self.__tplPath, template), os.F_OK):
                    file = open ("%s/%s/logon.bat" \
                                  % (self.__tplPath, template))
                    for line in file.readlines ():
                        self.__logonU.writelines (line)
                    self.__logonU.writelines ("\r\n")
                    file.close ()
                if os.access ("%s/%s/logon_%s.bat" % (self.__tplPath, template, self.__arch), os.F_OK):
                    file = open ("%s/%s/logon_%s.bat" \
                                  % (self.__tplPath, template, self.__arch))
                    for line in file.readlines ():
                        self.__logonU.writelines (line)
                    self.__logonU.writelines ("\r\n")
                    file.close ()
              
        except OSError:
            print "Can't write %s logon in %s/%s.bat" % (template, self.__user, self.__computer)