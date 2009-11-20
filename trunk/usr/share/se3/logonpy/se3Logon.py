# -*- coding: utf-8 -*-
import sys, os, posix
from se3Utils import *

class se3Logon:

    def __init__ (self, path2BatFiles, path2Templates, user, computer, master, arch):
        """
            Open logon bat, some initializations
        """
        try: 
            self.__logonU = open ("%s/machine/%s/logon.bat" % (path2BatFiles, computer), 'w')
            self.__logonC = open ("%s/machine/%s/startup.bat" % (path2BatFiles, computer), 'w')
            self.__logoffU = open ("%s/machine/%s/logoff.bat" % (path2BatFiles, computer), 'w')
            self.__logoffC = open ("%s/machine/%s/shutdown.bat" % (path2BatFiles, computer), 'w')
            self.__logonU.write ("cscript C:\Windows\printers.vbs\r\n")
            self.__logonC.write ("cscript C:\Windows\printers.vbs\r\n")

            self.__tplPath = path2Templates
            self.__batPath = path2BatFiles
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
            if not os.access ("%s/machine/%s/gpt.ini" % (self.__batPath, self.__computer), os.F_OK):
	            self.__logonU.write ("gpupdate /force\r\n")
            else:
                    self.__logonU.write ("gpupdate /Target:computer /force\r\n")
            self.__logonC.write ("reg add \"HKEY_USERS\.DEFAULT\Control Panel\Keyboard\" /v InitialKeyboardIndicators /d 2 /f\r\n") # not working with gpo

            if self.__arch == "Vista":
                # Remove public folder from explorer
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\explorer\Desktop\NameSpace\{4336a54d-038b-4685-ab02-99bb52d3fb8b} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\explorer\Desktop\NameSpace\{4336a54d-038b-4685-ab02-99bb52d3fb8b} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\explorer\Desktop\NameSpace\{59031a47-3f72-44a7-89c5-5595fe6b30ee} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\explorer\Desktop\NameSpace\{59031a47-3f72-44a7-89c5-5595fe6b30ee} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wpkg\running /f\r\n")

            self.__logoffC.write ("del /Q /S /F %SYSTEMDRIVE%\windows\system32\GroupPolicy\User\r\n")
            self.__logoffU.write ("del /Q /S /F %USERPROFILE%\Application Data\Microsoft\Wallpaper1.bmp\r\n")
            self.__logonU.close ()
            self.__logonC.close ()
            self.__logoffU.write ("\r\n")
            self.__logoffC.write ("\r\n")
            self.__logoffU.close ()
            self.__logoffC.close ()
            
        except OSError:
           print "Can't write %s/%s.bat" % (self.__user, self.__computer)


    def winsAdd (self):
        """
            Restrictions rules
        """
        try:
            self.__logonC.write ("nbtstat -RR\r\n")

        except OSError:
            print "Can't write admin %s.bat" %  self.__computer


    def addFirefoxAutoConfig (self):
        """
            Add firefox autconfig files to logon script
        """
        try:
            self.__logonC.write ("cacls C:\Windows\System32\GroupPolicy\User\\registry.pol /E /G adminse3:F\r\n")
            self.__logonC.write ("cacls C:\Windows\System32\GroupPolicy\User\Scripts\scripts.ini /E /G adminse3:F\r\n")
            self.__logonC.write ("cacls C:\Windows\System32\GroupPolicy\User\Scripts\Logon\logon.bat /E /G adminse3:F\r\n")
            self.__logonC.write ("cacls C:\Windows\System32\GroupPolicy\User\Scripts\Logoff\logoff.bat /E /G adminse3:F\r\n")
            self.__logonC.write ("Set FIREFOXCFG=%ProgramFiles%\\Mozilla Firefox\\firefox.cfg\r\n")
            self.__logonC.write ("Set ALLJS=%ProgramFiles%\\Mozilla Firefox\\greprefs\\all.js\r\n")
            self.__logonC.write ("echo //BEGIN CE prefs >\"%FIREFOXCFG%\"\r\n")
            self.__logonC.write ("echo lockPref(\"autoadmin.global_config_url\", \"http://%s:909/firefox-profile.php?username=\" + getenv(\"USERNAME\") + \"&computername=\" + getenv(\"COMPUTERNAME\") + \"&userdomain=\" + getenv(\"USERDOMAIN\") + \"?\"); >>\"%%FIREFOXCFG%%\"\r\n" % self.__master)
            self.__logonC.write ("find \"general.config.obscure_value', 0\" \"%ALLJS%\" || echo pref('general.config.obscure_value', 0); >> \"%ALLJS%\"\r\n")
            self.__logonC.write ("find \"general.config.filename\" \"%ALLJS%\" || echo pref('general.config.filename', 'firefox.cfg'); >> \"%ALLJS%\"\r\n")
            self.__logonC.write ("net time \\\\%s\r\n" % self.__master)
        except: pass


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
                        if self.__arch == "Vista" and line.find ("net use") != -1 \
                                                  and line.find ("persistent") == -1:
                            line = line[:-2] + (" /persistent:no\r\n")
                        if line.find ("se3printers.bat") == -1:
                            self.__logonU.writelines (line)
                    self.__logonU.writelines ("\r\n")
                    file.close ()
                if os.access ("%s/%s/logon_%s.bat" % (self.__tplPath, template, self.__arch), os.F_OK):
                    file = open ("%s/%s/logon_%s.bat" \
                                  % (self.__tplPath, template, self.__arch))
                    for line in file.readlines ():
                        if self.__arch == "Vista" and line.find ("net use") != -1 \
                                                  and line.find ("persistent") == -1:
                            line = line[:-2] + (" /persistent:no\r\n")
                        if line.find("se3printers.bat") == -1:
                            self.__logonU.writelines (line)
                    self.__logonU.writelines ("\r\n")
                    file.close ()
                if os.access ("%s/%s/startup.bat" % (self.__tplPath, template), os.F_OK):
                    file = open ("%s/%s/startup.bat" \
                                  % (self.__tplPath, template))
                    for line in file.readlines ():
                        self.__logonC.writelines (line)
                    self.__logonC.writelines ("\r\n")
                    file.close ()
	
        except OSError:
            print "Can't write %s logon in %s/%s.bat" % (template, self.__user, self.__computer)


    def addTemplateslogoff (self, templates):
        """
            Add templates logoff, ignore se3printers.bat
        """
        try:
            for template in templates:
                if os.access ("%s/%s/logoff.bat" % (self.__tplPath, template), os.F_OK):
                    file = open ("%s/%s/logoff.bat" \
                                  % (self.__tplPath, template))
                    for line in file.readlines ():
                        self.__logoffU.writelines (line)
                    self.__logoffU.writelines ("\r\n")
                    file.close ()
                if os.access ("%s/%s/logoff_%s.bat" % (self.__tplPath, template, self.__arch), os.F_OK):
                    file = open ("%s/%s/logoff_%s.bat" \
                                  % (self.__tplPath, template, self.__arch))
                    for line in file.readlines ():
                        self.__logoffU.writelines (line)
                    self.__logoffU.writelines ("\r\n")
                    file.close ()
                if os.access ("%s/%s/shutdown.bat" % (self.__tplPath, template), os.F_OK):
                    file = open ("%s/%s/shutdown.bat" \
                                  % (self.__tplPath, template))
                    for line in file.readlines ():
                        self.__logoffC.writelines (line)
                    self.__logoffC.writelines ("\r\n")
                    file.close ()

        except OSError:
            print "Can't write %s logoff in %s/%s.bat" % (template, self.__user, self.__computer)
    def addReglogon (self):
        """
            Add regedit job at logon
        """
        try:
            if os.access ("%s/machine/%s/user.reg" % (self.__batPath, self.__computer), os.F_OK):
                self.__logonU.writelines ("\\\\%s\Netlogon\Cpau.exe -wait -lwop -hide -dec -file \\\\%s\Netlogon\Machine\Reg_helper.job\r\n" \
                % (self.__master, self.__master))
        except OSError:
            print "Can't write reg file for user %s and computer %s logon.bat" % (self.__user, self.__computer)
