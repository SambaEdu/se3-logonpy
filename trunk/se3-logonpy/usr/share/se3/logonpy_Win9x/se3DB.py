# -*- coding: utf-8 -*-
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

        if os.access ("/var/se3/Docs/media/fonds_ecran/%s.jpg" % self.__user, os.F_OK) \
            and self.__arch != "Win95":
            wallModule = True

        cursor = self.__db.cursor()
        for template in templates:
            cursor.execute ("SELECT CleID, valeur from restrictions where groupe=%s", template)
            for result in cursor.fetchall ():
                results[result[0]] = result[1]

        for key in results.keys():
            cursor.execute ("SELECT Chemin, Genre, OS FROM corresp where CleID='%s'\
                                    and (OS like \"*Win9x*\" or OS=\"TOUS\")", key)
            row2 = cursor.fetchone ()

            if row2 != None:
                rest.append ((row2[0], row2[1], row2[2], results[key]))

        cursor.close ()

        return rest
