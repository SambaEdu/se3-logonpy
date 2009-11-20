# -*- coding: utf-8 -*-
import sys, os

class se3Profile:

    def __init__ (self, user):
        """
            Init Profile
        """
        self.__user = user


    def __del__ (self):
        """
            Del Profile
        """
 
    def lock (self):
        """
            Lock user profile
        """
        try:
            if os.access ("/home/profiles/%s/ntuser.dat" % self.__user, os.F_OK):
                self.__chmod ("/home/profiles/%s" % self.__user, 0500)
                os.rename ("/home/profiles/%s/ntuser.dat" % self.__user, \
                           "/home/profiles/%s/ntuser.man" % self.__user)
							  
        except OSError:
            print "Can't lock profile"
	

    def unlock (self):
        """
            Unlock user profile
        """
        try:
            if os.access ("/home/profiles/%s/ntuser.man" % self.__user, os.F_OK):
                self.__chmod("/home/profiles/%s" % self.__user, 0700)
                os.rename ("/home/profiles/%s/ntuser.man" % self.__user, \
                           "/home/profiles/%s/ntuser.dat" % self.__user)
							  
        except OSError:
            print "Can't unlock profile"
	

    def __chmod (self, dirPath, mode):
        """
            Recursive dir chmod
        """
        os.chmod (dirPath, mode)
        for root, dirs, files in os.walk (dirPath, False):
            for name in files:
                os.chmod (os.path.join (root, name), mode)
            for name in dirs:
                os.chmod (os.path.join (root, name), mode)

