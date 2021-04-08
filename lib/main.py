#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame

# YASP common imports
import sys
from constants import Constants

from title_screen import TitleScreen
from boot_screen import BootScreen
from game import Game
from preferences import Preferences


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()

        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.w = int(self.screen_h * 1.2)
        self.h = int(self.screen_h * 0.8)

        self.preferences = Preferences()
        self.fullscreen = self.preferences.get("fullscreen")
        self.go_mode()

        pygame.mouse.set_visible(False)

        pygame.display.set_caption(Constants.CAPTION)

    def go_mode(self):
        if self.fullscreen:
            self.mode = (self.screen_w, self.screen_h)
            if self.mode not in pygame.display.list_modes():
                self.mode = pygame.display.list_modes()[0]
            self.screen = pygame.display.set_mode(self.mode, pygame.FULLSCREEN)
        else:
            self.mode = (self.w, self.h)
            self.screen = pygame.display.set_mode(self.mode)
        self.unit = int(self.mode[1]/Constants.UNITS)

    def main(self):
        self.boot_screen()
        while True:
            if not self.title_screen():
                break
            if self.preferences.edit_flag:
                self.preferences.save()
                fullscreen = self.preferences.get('fullscreen')
                if self.fullscreen != fullscreen:
                    self.fullscreen = fullscreen
                    self.go_mode()
            else:
                self.play_game()

    def boot_screen(self):
        bs = BootScreen(self.screen, self.unit)
        bs.main()
        return bs.running

    def title_screen(self):
        self.go_mode()
        ts = TitleScreen(self.screen, self.unit, self.preferences)
        ts.main()
        return ts.running

    def play_game(self):
        gm = Game(self.screen, self.unit, self.preferences)
        gm.main()
        return gm.running


def main():
    game = Main()
    game.main()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
