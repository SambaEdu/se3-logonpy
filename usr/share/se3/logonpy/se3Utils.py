# -*- coding: utf-8 -*-
import os

def touch (path):
    """
        Create an empty file
    """
    try:
        file = open (path, 'w')
        file.close()
    except: pass
    
def remove (path):
    """
        Del user profile
    """
    try:
        for root, dirs, files in os.walk (path, False):
            for name in files:
                os.remove (os.path.join (root, name))
            for name in dirs:
                os.rmdir (os.path.join (root, name))
        os.rmdir (path)
    except: pass

