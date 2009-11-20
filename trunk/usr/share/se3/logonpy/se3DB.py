# -*- coding: utf-8 -*-
# $Id$
import sys, MySQLdb, os
sys.path.append('/etc/se3/python/')
from  mysqlinfo import *

class se3DB:

    def __init__ (self,user, arch):
        """
            Connect to se3db base 
        """
        try:
            self.__db = MySQLdb.connect(dbhost, dbuser, dbpass, dbname)
            self.__user = user
            self.__arch = arch
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)

    def __del__ (self):
        """
            Close connexion
        """
        self.__db.close ()

    def getValue (self, name):
        """
            Get a value from params table
        """
        try:
            cursor = self.__db.cursor ()
            cursor.execute ("SELECT value FROM params where name = %s" , name)
            row = cursor.fetchone ()
            cursor.close ()
            return row[0]

        except TypeError:
            return 0


    def setValue (self, name, value):
        """
            Set a value in params table
        """
        query = "UPDATE params SET  value = '" + value + \
                "' where name = '" + name + "'"
        cursor = self.__db.cursor ()
        cursor.execute ("UPDATE params SET value = %s WHERE name = %s" ,\
                        (value, name))
        cursor.close ()

    def getRestrictions(self, templates):
        """
            Return restriction list for a template
        """
        results = {}
        rest = []
        wallModule = False
        tileWallSet = False

        if ( os.access ("/var/se3/Docs/media/fonds_ecran/%s.bmp" % self.__user, os.F_OK) or \
           os.access ("/var/se3/Docs/media/fonds_ecran/%s.jpg" % self.__user, os.F_OK) ):
            wallModule = True

        cursor = self.__db.cursor()
        for template in templates:
            cursor.execute ("SELECT CleID, valeur from restrictions where groupe=%s", template)
            for result in cursor.fetchall ():
                results[result[0]] = result[1]

        for key in results.keys():
            cursor.execute ("SELECT Chemin, Genre, OS FROM corresp where CleID='%s'\
                                    and OS!=\"Win9x\"", key)
            row2 = cursor.fetchone ()

            if row2 != None:
                # Disable wallpaper key if wall module active
                if wallModule:
                    if not row2[0] in "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\ClassicShell" \
                                      "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\ForceActiveDesktopOn" \
                                      "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop\NoHTMLWallpaper":
                    
                        rest.append ((row2[0], row2[1], row2[2], results[key]))
                    if row2[0] == "HKEY_CURRENT_USER\Control Panel\Desktop\TileWallpaper":
                        tileWallSet = True
                        rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\WallpaperStyle",\
                              "REG_SZ", "2000,XP,Vista,Seven", results[key]))
                else:
                    rest.append ((row2[0], row2[1], row2[2], results[key]))

        cursor.close ()

        if wallModule:
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\ClassicShell",\
                         "REG_DWORD", "Vista,Seven", "SUPPR"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\ForceActiveDesktopOn",\
                         "REG_DWORD", "2000,XP", "0"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\ForceActiveDesktopOn",\
                         "REG_DWORD", "Vista,Seven", "1"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\NoActiveDesktop",\
                         "REG_DWORD", "2000,XP", "1"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop\NoChangingWallpaper",\
                         "REG_DWORD", "2000,XP,Vista,Seven", "1"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop\NoHTMLWallpaper",\
                         "REG_DWORD", "Vista,Seven", "SUPPR"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\Wallpaper",\
                         "REG_SZ", "2000,XP", "C:\Windows\Web\Wallpaper\Se3.bmp"))
            rest.append (("HKEY_CURRENT_USER\Control Panel\Desktop\Wallpaper",\
                         "REG_SZ", "2000,XP", "C:\Windows\Web\Wallpaper\Se3.bmp"))
            rest.append (("HKEY_CURRENT_USER\Control Panel\Desktop\Wallpaper",\
                         "REG_DWORD", "2000,XP", "PROTECT"))
            rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\Wallpaper",\
              		 	 "REG_SZ", "Vista,Seven", "C:\Windows\Web\Wallpaper\Se3.jpg"))
            rest.append (("HKEY_CURRENT_USER\Control Panel\Desktop\Wallpaper",\
  		 	             "REG_SZ", "Vista,Seven", "C:\Windows\Web\Wallpaper\Se3.jpg"))
            if not tileWallSet:
                rest.append (("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\WallpaperStyle",\
                         "REG_SZ", "2000,XP,Vista,Seven", "2"))
        return rest
