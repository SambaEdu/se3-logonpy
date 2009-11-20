# -*- coding: utf-8 -*-
import sys, os, posix
from se3Utils import *

class se3Printers:

    def __init__ (self, path2BatFiles, user, computer, master):
        """
            Open vbs registry rules, some initializations
        """
        try:
            self.__vbs = open ("%s/machine/%s/printers.vbs" % (path2BatFiles, computer), 'w')
            self.__user = user
            self.__computer = computer
            self.__master = master
            self.__vbsContent = []

            # Add some helpers
            if os.access ("/etc/se3/python/logonPrinters.vbs", os.F_OK):
                file = open ("/etc/se3/python/logonPrinters.vbs")
                for line in file.xreadlines ():
                    self.__vbsContent.append (line)
            
        except OSError:
            print "Can't write printer %s.vbs" % self.__computer
            sys.exit (1)


    def __del__ (self):
        """
            close vbs
        """
        try:
            for line in self.__vbsContent:
                self.__vbs.write (line)
          
            self.__vbs.close ()

        except OSError:
            print "Can't write printer %s.vbs" % self.__computer


    def add (self, printers):
        """
            Add printers rules
        """
        try:
            if (len (printers)):
                self.__vbsContent.append ("AddUserPrinterDevice \"%s\", \"%s\"\r\n" % (self.__master,printers[0]))
                self.__vbsContent.append ("SetUserDefaultPrinterDevice \"%s\", \"%s\"\r\n" % (self.__master, printers[0]))
                for printer in printers[1:]:
                    self.__vbsContent.append ("AddUserPrinterDevice \"%s\", \"%s\"\r\n" % (self.__master, printer))

        except OSError:
           print "Can't write printer %s.vbs" % self.__computer


    def clean (self):
        """
            Remove old printers
        """
        try:
            self.__vbsContent.append ("DeleteUserPrintersDevice \"%s\"\r\n" % self.__master)
            
        except OSError:
            print "Can't write printer %s.vbs" % self.__computer