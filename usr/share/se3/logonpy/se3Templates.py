# -*- coding: utf-8 -*-
import sys, os, posix

class se3Templates:

    def __init__ (self, path2Templates,path2BatFiles, user):
        """
            Initializations
        """
        self.__user = user
        self.__tplPath = path2Templates


    def getTemplates (self):
        """
            Get template dir list
        """
        try:
            dirList = []
            for dir in os.listdir (self.__tplPath):
                 if os.path.isdir (os.path.join(self.__tplPath, dir)):
                     dirList.append (dir.lower ())
            return dirList
        except OSError:
            print "Error getting template list"

    def createDesktop (self, templates):
        """
            Create destktop from templates
        """
        try:
            for template in templates:
                list = self.__getDirListing ("%s/%s/Bureau" % \
                                             (self.__tplPath, template), False)
                for item in list:
                    self.__createLinks (item, template)
        except OSError:
            print "Error while creating desktop"

# afin que le bureau puisse gerer des icones placées dans des repertoires
# décommenter les 2 fonctions ci dessous et commenter la fonction cleandesktop
#	
#   def cleandir (self, dir):
#        """
#            efface tout les liens contenus dans le repertoire dir
#        """
#        try:
#             list = os.listdir (dir)
#             for item in list:
#                 if os.path.islink (dir + item):
#                     print "Effacement du lien symbolique " + dir + item
#                     self.__removeLinks (dir + item)
#                 else :
#                     if os.path.isdir (dir  + item):
#                         self.cleandir (dir + item + "/")
#                         if os.listdir (dir + item + "/") == []:
#                             print "Le repertoire " + dir + item + "/ est vide on l efface"
#                             os.rmdir  (dir + item)
#        except OSError:
#            print "Error while cleaning repertoire " + dir + item
#
# def cleanDesktop (self):
#        """
#            Remove all links on desktop
#        """
#        try:
#            dir = "/home/%s/profil/Bureau/" % self.__user
#            self.cleandir (dir)
#        except OSError:
#            print "Error while cleaning desktop"
	

    def cleanDesktop (self):
        """
            Remove all links on desktop
        """
        try:
#            list = os.listdir ("/home/%s/profil/Bureau" % \
#                                         (self.__user))
	    dir = "/home/%s/profil/Bureau/" % self.__user
	    list = os.listdir (dir)
            for item in list:
                self.__removeLinks (dir + item)

        except OSError:
            print "Error while cleaning desktop"


    def createStartMenu (self, templates):
        """
            Create start menu from templates
        """
        try:
            for template in templates:
                list = self.__getDirListing ("%s/%s/Demarrer" % \
                                             (self.__tplPath, template), False)
                for item in list:
                    self.__createLinks (item, template)
        except OSError:
            print "Error while creating start menu"


    def cleanStartMenu (self):   
          """   
              Remove all links in start menu   
          """   
          try:   
              list = self.__getDirListing ("/home/%s/profil/Demarrer" % \
                                           (self.__user), True)   
              for item in list:   
                  self.__removeLinks (item)   
      
          except OSError:   
              print "Error while cleaning desktop"


    def __createLinks (self, path, template):
        """
            Create file in user environnement from template
            path: absolute path to template file
        """
        item = path.replace ("/home/templates/%s/" % template, "")
        if os.path.isdir(path):
             if not os.access ("/home/%s/profil/%s" % (self.__user, item), os.F_OK):
                 os.mkdir ("/home/%s/profil/%s" % (self.__user, item))
        else:
            if not os.access ("/home/%s/profil/%s" % (self.__user, item), os.F_OK):
                posix.symlink ("%s" % path, "/home/%s/profil/%s" \
                                    % (self.__user, item))

    def __removeLinks (self, path):
        """
            Remove all dst links
        """
        try:
            if os.path.islink (path):
                os.unlink (path)
            else:
                os.rmdir (path)

        except OSError:
            # path is a dir, path is not empty
            return
        
    def __getDirListing (self, dirPath, revert):
        """
            Return a list with dir content
            Dirs first, then files
            if revert == True, Files first, then dirs, then subdirs
            else, Dirs first, then subdirs, then files
        """
        dirList = []
        fileList = []
        for root, dirs, files in os.walk (dirPath, False):
            for name in files:
                fileList.append (os.path.join (root, name))
            for name in dirs:
                dirList.append (os.path.join (root, name))
        
        if revert == True:
            return fileList + dirList
        else:
            dirList.reverse ()
            return dirList + fileList
