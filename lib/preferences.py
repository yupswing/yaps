#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pickle

# YASP common imports
from constants import Constants


class Preferences(object):
    def __init__(self):
        self.filename = Constants.PREFERENCES_FILE
        # default preferences [first run or missing file]
        self.default = {"fullscreen": False}
        self.edit_flag = False
        self.load()

    def get(self, key):
        return self.preferences.get(key, None)

    def set(self, key, value):
        self.edit_flag = True
        self.preferences[key] = value

    def load(self):
        self.preferences = {}
        pref_file = None
        try:
            pref_file = open(self.filename, "rb")
            self.preferences = pickle.load(pref_file)
        except:
            self.preferences = self.default
        finally:
            if pref_file:
                pref_file.close()

    def save(self):
        pref_file = None
        try:
            pref_file = open(self.filename, "wb")
            pickle.dump(self.preferences, pref_file)
        except:
            pass
        finally:
            if pref_file:
                pref_file.close()
        self.edit_flag = False
