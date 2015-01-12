#
#  YetAnotherPythonSnake 0.91
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://imente.it
#  Licence: (CC) BY-NC 3.0 [http://creativecommons.org/licenses/by-nc/3.0/]
#

import pygame
import random
import pickle

#YASP common imports
import data
import util
from constants import Constants

class Preferences(object):
    def __init__(self):
        self.filename = Constants.PREFERENCES_FILE
        self.default = {"fullscreen":False} # default preferences [first run or missing file]
        self.edit_flag = False
        self.load()

    def get(self,key):
        return self.preferences.get(key,None)

    def set(self,key,value):
        self.edit_flag = True
        self.preferences[key] = value

    def load(self):
        self.preferences = {}
        pref_file = None
        try:
            pref_file = open(self.filename,"rb")
            self.preferences = pickle.load(pref_file)
        except:
            self.preferences = self.default
        finally:
            if pref_file: pref_file.close()

    def save(self):
        pref_file = None
        try:
            pref_file = open(self.filename,"wb")
            pickle.dump(self.preferences,pref_file)
        except:
            pass
        finally:
            if pref_file: pref_file.close()
        self.edit_flag = False
