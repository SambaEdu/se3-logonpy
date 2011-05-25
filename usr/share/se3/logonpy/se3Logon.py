# -*- coding: utf-8 -*-
import sys, os, posix
from se3Utils import *

class se3Logon:

    def __init__ (self, path2BatFiles, path2Templates, user, computer, master, arch, urlse3):
        """
            Open logon bat, some initializations
        """
        try: 
            self.__logonU = open ("%s/machine/%s/logon.cmd" % (path2BatFiles, computer), 'w')
            self.__logonC = open ("%s/machine/%s/startup.cmd" % (path2BatFiles, computer), 'w')
            self.__logoffU = open ("%s/machine/%s/logoff.cmd" % (path2BatFiles, computer), 'w')
            self.__logoffC = open ("%s/machine/%s/shutdown.cmd" % (path2BatFiles, computer), 'w')
            self.__logonU.write ("cscript %SYSTEMROOT%\Printers.vbs\r\n")
            self.__logonC.write ("cscript %SYSTEMROOT%\Printers.vbs\r\n")
            self.__logonC.write ("echo Machine ok>%SYSTEMROOT%\System32\Grouppolicy\Se3.log\r\n")
            self.__logoffC.write ("del /s /f /q %SYSTEMROOT%\System32\Grouppolicy\Se3.log\r\n")

            self.__tplPath = path2Templates
            self.__batPath = path2BatFiles
            self.__user = user
            self.__computer = computer
            self.__master = master
            self.__arch = arch
            self.__urlse3 = urlse3

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
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{4336a54d-038b-4685-ab02-99bb52d3fb8b} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{4336a54d-038b-4685-ab02-99bb52d3fb8b} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{59031a47-3f72-44a7-89c5-5595fe6b30ee} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{59031a47-3f72-44a7-89c5-5595fe6b30ee} /f\r\n")
                self.__logonC.write ("reg delete HKEY_LOCAL_MACHINE\Software\Wpkg\Running /f\r\n")

            self.__logonU.write ("time /T >> %SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logonU.write ("---logon.cmd de %USERNAME%--->> %SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logonC.write ("del /Q /S /F %SYSTEMROOT%\System32\GroupPolicy\User\r\n")
            self.__logoffC.write ("del /Q /S /F %SYSTEMROOT%\System32\GroupPolicy\User\r\n")
            self.__logoffU.write ("del /Q /S /F %USERPROFILE%\Application Data\Microsoft\Wallpaper1.bmp\r\n")
            self.__logonU.write ("del /Q /S /F %SYSTEMROOT%\System32\GroupPolicy\User\Registry.pol>>%SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logoffU.write ("del /Q /S /F %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\Logon\Logon.cmd>>%SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logoffU.write ("del /Q /S /F %SYSTEMROOT%\Web\Wallpaper\Se3.*>>%SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logonU.close ()
            self.__logonC.close ()
            self.__logoffU.write ("\r\n")
            self.__logoffC.write ("\r\n")
            self.__logoffU.close ()
            self.__logoffC.close ()
            
        except OSError:
           print "Can't write %s/%s.cmd" % (self.__user, self.__computer)


    def winsAdd (self):
        """
            Restrictions rules
        """
        try:
            self.__logonC.write ("nbtstat -RR\r\n")

        except OSError:
            print "Can't write admin %s.cmd" %  self.__computer


    def addFirefoxAutoConfig (self):
        """
            Add firefox autconfig files to logon script
        """
        try:
#           self.__logonC.write ("cacls %SYSTEMROOT%\System32\GroupPolicy\User\\registry.pol /E /G adminse3:F\r\n")
#            self.__logonC.write ("cacls %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\scripts.ini /E /G adminse3:F\r\n")
#            self.__logonC.write ("cacls %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\Logon\logon.cmd /E /G adminse3:F\r\n")
#            self.__logonC.write ("cacls %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\Logoff\logoff.cmd /E /G adminse3:F\r\n")
            self.__logonC.write ("Set FIREFOXCFG=%ProgramFiles%\\Mozilla Firefox\\firefox.cfg\r\n")
            self.__logonC.write ("Set ALLJS=%ProgramFiles%\\Mozilla Firefox\\greprefs\\all.js\r\n")
            self.__logonC.write ("echo //BEGIN CE prefs >\"%FIREFOXCFG%\"\r\n")
            self.__logonC.write ("echo lockPref(\"autoadmin.global_config_url\", \"%s/firefox-profile.php?username=\" + getenv(\"USERNAME\") + \"&computername=\" + getenv(\"COMPUTERNAME\") + \"&userdomain=\" + getenv(\"USERDOMAIN\") + \"?\"); >>\"%%FIREFOXCFG%%\"\r\n" % self.__urlse3)
            self.__logonC.write ("find \"general.config.obscure_value', 0\" \"%ALLJS%\" || echo pref('general.config.obscure_value', 0); >> \"%ALLJS%\"\r\n")
            self.__logonC.write ("find \"general.config.filename\" \"%ALLJS%\" || echo pref('general.config.filename', 'firefox.cfg'); >> \"%ALLJS%\"\r\n")
            self.__logonC.write ("net time \\\\%s\r\n" % self.__master)
        except: pass


    def addgetGPOversion (self):
        """
            get GPO version from registry and write it to gpt.ini
        """
        try:
            self.__logonC.write ("for /f \"tokens=2 delims=x\" %%a in ('reg query \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Group Policy\\State\\Machine\\GPO-List\\0\" /v Version ^| findstr REG_DWORD') do set /a VERSION=0x%%a\r\n")
            self.__logonC.write ("if \"%VERSION%\"==\"\" set VERSION=65537\r\n")           
            self.__logonC.write ("echo [general]>%SYSTEMROOT%\\System32\\GroupPolicy\\gpt.ini\r\n")
            self.__logonC.write ("echo Version=%VERSION%>>%SYSTEMROOT%\\System32\\GroupPolicy\\gpt.ini\r\n")
            self.__logonC.write ("echo gPCUserExtensionNames=[{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{0F6B957E-509E-11D1-A7CC-0000F87571E3}][{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B66650-4972-11D1-A7CA-0000F87571E3}]>>%SYSTEMROOT%\\System32\\GroupPolicy\\gpt.ini\r\n")
            self.__logonC.write ("echo gPCMachineExtensionNames=[{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{0F6B957D-509E-11D1-A7CC-0000F87571E3}][{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B6664F-4972-11D1-A7CA-0000F87571E3}]>>%SYSTEMROOT%\\System32\\GroupPolicy\\gpt.ini\r\n")
            self.__logonC.write ("time /T >> %SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logonC.write ("echo GPO startup ok>> %SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
            self.__logonC.write ("echo %VERSION%>> %SYSTEMDRIVE%\\netinst\\logs\\domscripts.txt\r\n")
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
            print "Can't write reg file for user %s and computer %s logon.cmd" % (self.__user, self.__computer)
