# -*- coding: utf-8 -*-
from struct import pack

REG_NONE=0
REG_SZ=1
REG_EXPAND_SZ=2
REG_BINARY=3
REG_DWORD=4
REG_DWORD_BIG_ENDIAN=5
REG_LINK=6
REG_MULTI_SZ=7
REG_RESOURCE_LIST=8
REG_FULL_RESOURCE_DESCRIPTOR=9
REG_RESOURCE_REQUIREMENTS_LIST=10
REG_QWORD=11;

REGFILE_SIGNATURE="67655250"
REGFILE_VERSION="00000001"

folder_keys = [('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\{374DE290-123F-4565-9164-39C4925E467B}', 'REG_EXPAND_SZ', 'Vista', 'K:\Bureau'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Local AppData', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', '%USERPROFILE%\Application Data'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Local Settings', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', '%USERPROFILE%\Local Settings'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\AppData', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\\appdata'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Cache', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\Cache'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Cookies', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\Cookies'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Desktop', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\Bureau'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Favorites', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\Favorites'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\History', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\History'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\My Music', 'REG_EXPAND_SZ', 'Vista', 'K:\Musique'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\My Pictures', 'REG_EXPAND_SZ', 'Vista', 'K:\Photos'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\My Video', 'REG_EXPAND_SZ', 'Vista', 'K:\Videos'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\NetHood', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\NetHood'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Personal', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\Docs'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\PrintHood', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\PrintHood'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Recent', 'REG_EXPAND_SZ', 'Vista', 'K:\profil\\appdata\Recent'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\SendTo', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven','%USERPROFILE%\SendTo'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Templates', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\\appdata\Templates'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Programs', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\Demarrer\Programmes'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Start Menu', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\Demarrer'),
              ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Startup', 'REG_EXPAND_SZ', '2000,XP,Vista,Seven', 'K:\profil\Demarrer\Programmes\Démarrage'.decode('utf8').encode('iso-8859-15'))]

default_keys = [('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\HideLegacyLogonScripts', 'REG_DWORD', 'XP', '1'),
                ('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\TcpNumConnections', 'REG_DWORD', '2000,XP,Vista,Seven', '5000'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\DeleteRoamingCache', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System\DeleteRoamingCache', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\RunLogonScriptSync', 'REG_DWORD', 'Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\RunLogonScriptSync', 'REG_DWORD', '2000,XP', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System\WaitForNetwork', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows NT\CurrentVersion\Winlogon\SyncForegroundPolicy', 'REG_DWORD', 'XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\ShowLogonOptions', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\DisableCAD', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system\DontDisplayLastUserName', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_ShowMyDocs', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_ShowMyPics', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_ShowMyMusic', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_ShowMyGames', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_ShowUser', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\KnownFolder\{374DE290-123F-4565-9164-39C4925E467B}\NukeOnDelete', 'REG_DWORD', 'Vista', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\KnownFolder\{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}\NukeOnDelete', 'REG_DWORD', 'Vista', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\KnownFolder\{FDD39AD0-238F-46AF-ADB4-6C85480369C7}\NukeOnDelete', 'REG_DWORD', 'Vista', '1'),
                ('HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\NetCache\NoConfigCache', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\NetCache\DisableFRAdminPin', 'REG_DWORD', '2000,XP,Vista,Seven', '2'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel\{645FF040-5081-101B-9F08-00AA002F954E}', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\ClassicStartMenu\{645FF040-5081-101B-9F08-00AA002F954E}', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\WindowsWelcomeCenter', 'REG_SZ', 'Vista', 'SUPPR'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\A7066653-8D6C-40A8-910E-A1F54B84C7E5\ACSettingIndex', 'REG_DWORD', 'Vista', '2'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\A7066653-8D6C-40A8-910E-A1F54B84C7E5\DCSettingIndex', 'REG_DWORD', 'Vista', '2'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\94ac6d29-73ce-41a6-809f-6363ba21b47e\ACSettingIndex', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\94ac6d29-73ce-41a6-809f-6363ba21b47e\DCSettingIndex', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\\abfc2519-3608-4c2a-94ea-171b0ed546ab\ACSettingIndex', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Power\PowerSettings\\abfc2519-3608-4c2a-94ea-171b0ed546ab\DCSettingIndex', 'REG_DWORD', 'Vista', '0'),
                ('HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\System\ExcludeProfileDirs', 'REG_SZ', '2000,XP,Vista,Seven', 'Application Data;Temporary Internet Files;Historique;Temp;Credentials;Media Player;Windows Media;SystemCertificates;CrypnetUrlCache;Internet Explorer'),
                ('HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\DisablePasswordChange', 'REG_DWORD', '2000,XP,Vista,Seven', '1'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Windows NT\Printers\KMPrintersAreBlocked', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows NT\Printers\PointAndPrint\Restricted', 'REG_DWORD', 'XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{42B5FAAE-6536-11d2-AE5A-0000F87571E3}\NoGPOListChanges', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{42B5FAAE-6536-11d2-AE5A-0000F87571E3}\NoSlowLink', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{42B5FAAE-6536-11d2-AE5A-0000F87571E3}\NoBackgroundPolicy', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{35378EAC-683F-11D2-A89A-00C04FBBCFA2}\NoBackgroundPolicy', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{35378EAC-683F-11D2-A89A-00C04FBBCFA2}\NoGPOListChanges', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Group Policy\{35378EAC-683F-11D2-A89A-00C04FBBCFA2}\NoSlowLink', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System\SlowLinkDetectEnabled', 'REG_DWORD', '2000,XP,Vista,Seven', '0'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\HideFastUserSwitching', 'REG_DWORD', 'Vista', '1'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\SetVisualStyle', 'REG_EXPAND_SZ', 'XP', '%windir%\\resources\\themes\luna\luna.msstyles'),
                ('HKEY_CURRENT_USER\Control Panel\Colors\Background', 'REG_SZ', 'XP', '0 0 0'),
                ('HKEY_CURRENT_USER\Control Panel\Colors\MenuHilight', 'REG_SZ', 'XP', '49 106 197'),
                ('HKEY_CURRENT_USER\Control Panel\Colors\Hilight', 'REG_SZ', 'XP', '49 106 197'),
                ('HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\ThemeManager\ColorName', 'REG_SZ', 'XP', 'NormalColor'),
                ('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\NoDriveAutoRun', 'REG_DWORD', '2000,XP,Vista,Seven', '67108863')]
#TODO Remove all style keys, it's now ntuser.dat default!

class se3GPO:

    def __init__ (self, path2BatFiles, user, computer, arch, master):
        """
            Open pol file
        """
        try: 
            self.__gpoC = open ("%s/machine/%s/machine.pol" % (path2BatFiles, computer), 'wb')
            self.__gpoU = open ("%s/machine/%s/user.pol" % (path2BatFiles, computer), 'wb')
            self.__gpoC.write (self.__getDword (REGFILE_SIGNATURE))
            self.__gpoC.write (self.__getDword (REGFILE_VERSION))
            self.__gpoU.write (self.__getDword (REGFILE_SIGNATURE))
            self.__gpoU.write (self.__getDword (REGFILE_VERSION))
            self.__user = user
            self.__computer = computer
            self.__master = master
            self.__arch = arch

        except OSError:
            print "Can't create gpo for %s/%s" % (user, computer)
            sys.exit (1)


    def __del__ (self):
        """
            Close pol files
        """
        try:
            self.__gpoC.close()
            self.__gpoU.close()
            

        except OSError:
           print "Can't create gpo for %s/%s" % (user, computer)


    def __getByte (self, str):
        """
            Return byte from string
        """
        byte=""
        if len(str)>1:
            byte="%c" %int(str[0:2] ,16)
        else:
            byte="%c" % int(str[0]+'0', 16)
        return byte


    def __getDByte (self, str):
        """
            Return dbyte from string
        """
        if len(str)>2:
            return self.__getByte(str[0:2]) + self.__getByte(str[2:])
        else:
            return self.__getByte(str[0:2]) + self.__getByte("00")


    def __getDchar (self, str):
        l = len (str)
        if l>1:
            return "%c" % ord(str[0]) +  "%c" % ord(str[1])
        elif l == 1:
            return pack("H",  ord(str[0]))
        else:
            return self.__getByte("00")


    def __getDstring (self, str):
        """
            Return gpo string format
        """
        dstr=""
        for c in str:
            dstr+=self.__getDchar (c)
        dstr += self.__getDByte("00")
        return dstr


    def __getDstring_semi (self, str):
        """
            Return gpo string format with semi
        """
        dstr=""
        dstr = self.__getDstring(str)
        dstr += self.__getDchar(';')
        return dstr


    def __getDword (self, str):
        """
            Return dword
        """
        word=""
        for i in 0, 2, 4, 6:
            word+="%c" % int(str[i:i+2] ,16)
        return word[::-1]


    def __getBinaryString(self, str):
        """
            Return binary string
        """
        string = ""
        ristr = ""
        istr = "%X" % int(str)
        i = len (istr)
        if i == 1:
            i=0
            ristr = '0' + istr
        while i > 0:
            ristr += istr[i-2:i]
            i -= 2
        if i != 0:
            ristr += '0' + istr[0]

        ristr += (8 - len(ristr)) * '0'
        for i in 0, 2, 4, 6:
            string += "%c" % int(ristr[i:i+2], 16)

        return string


    def __getIntSemi(self, i) :
        """
            Return int with semi
        """
        istr = ""
        # Assuming 2 bytes max 
        tmp = i % 256;
        istr += chr(tmp);
    
        i -= tmp;
        tmp = i / 256;
        istr += chr(tmp);

        istr += self.__getDByte("00") + self.__getDchar(";")
        return istr


    def __polStr (self, key, value, type, data):
        """
            Return policy string for key value with type and data content
        """
        polStr = ""
        polStr += self.__getDchar ('[')
        polStr += self.__getDstring_semi (key)
        polStr += self.__getDstring_semi (value)
        polStr += self.__getIntSemi (type)
        if type == REG_SZ or type == REG_EXPAND_SZ or type == REG_MULTI_SZ:
            polStr += self.__getIntSemi ((len(data)+1)*2)
            polStr += self.__getDstring (data)
        else:
            polStr += self.__getIntSemi (REG_DWORD)
            polStr += self.__getBinaryString (data)
        polStr += self.__getDchar (']')
        return polStr


    # Local Vista GPO don't have default printer option, so, not useful as this.
    #def addPrinters (self, printers):
    #    """
    #        Add reg rules to pol
    #    """
    #    try:
    #        printers_key="Software\Policies\Microsoft\Windows NT\Printers\PushedConnections\\"
    #        for printer in printers:
    #            hexdata = self.__polGetAddValHex (printers_key + printer, "printAttributes", REG_DWORD, "0")
    #            hexdata += self.__polGetAddValHex (printers_key + printer, "printerName", REG_SZ, printer)
    #            hexdata += self.__polGetAddValHex (printers_key + printer, "serverName", REG_SZ, "\\\\" + self.__master)
    #            hexdata += self.__polGetAddValHex (printers_key + printer, "uNCName", REG_SZ, "\\\\" + self.__master + "\\" + printer)
    #            self.__gpoU.write (hexdata)
    #    except: pass


    def addRest (self, restrictions):
        """
            Add reg rules to pol
        """
        restrictions += folder_keys + default_keys
        try:
            for rest in restrictions:
                if rest[2] != "TOUS":
                    if self.__arch == "Win2K" and "2000" not in rest[2] :
                        continue
                    elif self.__arch == "WinXP" and "XP" not in rest[2] :
                        continue
                    elif self.__arch == "Vista" and "Vista" not in rest[2] :
                        continue
                    elif self.__arch == "Seven" and "Seven" not in rest[2] :
                        continue

                firstbackslash = rest[0].find("\\")
                lastbackslash = rest[0].rfind("\\")
                key = rest[0][firstbackslash+1:lastbackslash]
                value = rest[0][lastbackslash+1:]

                if rest[1] == "REG_DWORD":
                    type = REG_DWORD
                elif rest[1] == "REG_SZ":
                    type = REG_SZ
                elif rest[1] == "REG_EXPAND_SZ":
                    type = REG_EXPAND_SZ
                else:
                    continue # Unknown type

                try:
                    if rest[3] == "SUPPR":
                        hexdata = self.__polStr (key, "**Del."+value, type, "0")
                    elif rest[3] == "PROTECT":
                        hexdata = self.__polStr (key, "**SecureKey", REG_DWORD, "1")
                    elif rest[3] == "UNPROTECT":
                        hexdata = self.__polStr (key, "**SecureKey", REG_DWORD, "0")
                    else:
                        hexdata = self.__polStr (key, value, type, rest[3])

                    if rest[0].find("CURRENT_USER") != -1:
                        self.__gpoU.write (hexdata)
                    else:
                        self.__gpoC.write (hexdata)
                except:
                    print "La clef %s\%s est invalide!" % (key,value)

        except: pass
