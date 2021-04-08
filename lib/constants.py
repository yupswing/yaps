#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (me@simonecingano.it)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import os


class Constants:
    """ All of the in-game constants are declared here."""

    # GAME NAME
    CAPTION = "Yet Another Python Snake"
    UNITS = 53  # DO NOT MODIFY
    MAXSCORE = 15

    # FPS
    FPS = 15

    ALPHA = (255, 255, 0)

    START_LENGTH = 3

    HIGHSCORES_FILE = os.path.join('local', 'highscores')
    PREFERENCES_FILE = os.path.join('local', 'preferences')

    TIMERANGE_WALL = (1, 5)
    TIMERANGE_GOLD = (55, 65)

    GROW = 1

    CREDITS = """*Yet Another Python Snake (YAPS v0.94)
This game was made, as a personal exercise with python
and pygame, in a few days in June 2012
It's free, licensed under MIT Licence
Visit http://simonecingano.it for more info and the source code

*Design & Programming
Simone Cingano

*Sound & Music
NLM, Setuniman, Rock Savage, j1987, qubodup, theta4, Freqman
(CC) freesound.org

*Title Background
"Close up grass" by Sam Kim
(CC) flickr.com"""
