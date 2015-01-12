#
#  YetAnotherPythonSnake 0.9
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://imente.it
#  Licence: (CC) BY-NC 3.0 [http://creativecommons.org/licenses/by-nc/3.0/]
#

import os

class Constants:
    """ All of the in-game constants are declared here."""

    # GAME NAME
    CAPTION = "Yet Another Python Snake"
    UNITS = 53 # DO NOT MODIFY
    MAXSCORE = 15

    # FPS
    FPS = 15

    ALPHA = (255,255,0)

    START_LENGTH = 3

    HIGHSCORE = os.path.join('data','score','score.data')

    GROW = 1

    CREDITS = """*Yet Another Python Snake (YAPS v0.9)
This game was made, as a personal exercise with python
and pygame, in a few days in June 2012
It's free, licensed under Creative Commons BY-NC 3.0
Visit http://imente.it for more info and the source code

*Design & Programming
Simone Cingano

*Sound & Music
NLM, Setuniman, Rock Savage, j1987, qubodup, theta4, Freqman
(CC) freesound.org

*Title Background
"Close up grass" by Sam Kim
(CC) flickr.com"""
