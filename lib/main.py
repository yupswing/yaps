#
#  YetAnotherPythonSnake 0.9
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://imente.it
#  Licence: (CC) BY-NC 3.0 [http://creativecommons.org/licenses/by-nc/3.0/]
#

import pygame

#YASP common imports
import data
import util
from constants import Constants

from title_screen import TitleScreen
from boot_screen import BootScreen
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.mode = pygame.display.list_modes()[0]
        self.screen = pygame.display.set_mode(self.mode, pygame.FULLSCREEN)
        # self.mode = (1000,600)
        # self.screen = pygame.display.set_mode(self.mode)

        pygame.mouse.set_visible(False)


        self.unit = int(self.mode[1]/Constants.UNITS)
        pygame.display.set_caption(Constants.CAPTION)

    def main(self):
        self.boot_screen()
        while True:
            if not self.title_screen(): break
            self.play_game()

    def boot_screen(self):
        bs = BootScreen(self.screen, self.unit)
        bs.main()
        return bs.running

    def title_screen(self,):
        ts = TitleScreen(self.screen, self.unit)
        ts.main()
        return ts.running

    def play_game(self):
        gm = Game(self.screen, self.unit)
        gm.main()
        return gm.running

def main():
    game = Main()
    game.main()

if __name__ == "__main__":
    main()
