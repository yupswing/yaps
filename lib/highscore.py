#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import random

# YASP common imports
from constants import Constants


class Highscore(object):
    def __init__(self):
        self.filename = Constants.HIGHSCORE
        self.load()

    def cypher(self, text, direction=1):
        # stupid shifting to block stupid player from cheating highscore
        # Yes, I know, it's very easy to bypass :)
        r = 94
        o = 32
        result = ''
        if direction == 1:
            # create a seed and put it as first char
            seed = random.randint(0, r)+o
            result = chr(seed)
        else:
            # get the seed from first char
            seed = ord(text[0])
            text = text[1:]

        s = seed*direction
        ii = 1
        for char in text:
            x = ord(char)-32
            if x > r:
                continue
            x += s*ii  # shift
            x = x % r  # loop
            x += o  # remap
            result += chr(x)
            ii += 1
        return result

    def load(self):
        self.scores = []
        scores = []
        score_file = None
        try:
            score_file = open(self.filename, "rb")
            scores = [self.cypher(x, -1).split(',')
                      for x in score_file.read().split('\n') if x][:Constants.MAXSCORE]
        except:
            pass
        finally:
            if score_file:
                score_file.close()

        for el in scores:
            self.scores.append(
                {"score": el[2], "elapse": el[1], "name": el[0]})

    def save(self):
        score_file = None
        # try:
        score_file = open(self.filename, "wb")
        for el in self.scores:
            score_file.write(self.cypher("%s,%s,%s" %
                                         (el["name"], el["elapse"], el["score"]))+'\n')
        # except:
            # pass
        # finally:
        if score_file:
            score_file.close()

    def whereis(self, score, elapse):
        ii = -1
        for ii in range(len(self.scores)):
            el = self.scores[ii]
            if int(el["score"]) < int(score) or (int(el["score"]) == int(score) and str(el["elapse"]) > str(elapse)):
                return ii
        return ii+1

    def check(self, score, elapse):
        if self.whereis(score, elapse) < Constants.MAXSCORE:
            return True
        else:
            return False

    def insert(self, name, score, elapse):
        position = self.whereis(score, elapse)
        self.scores.insert(position, {"name": name.replace(
            ",", ""), "elapse": elapse, "score": str(score)})
        return position
