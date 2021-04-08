#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame

# YASP common imports
import data

# YASP imports
from object_foods import FoodBlock, FoodBlockKind


class Score(object):
    def __init__(self, unit, surface_rect):
        self.unit = unit
        self.image = pygame.Surface((self.unit*11, self.unit*11))
        self.rect = self.image.get_rect()
        self.rect.right = surface_rect.left
        self.rect.y = surface_rect.y
        self.score = 0
        self.seconds = 0
        self.length = 0
        self.font = pygame.font.Font(data.filepath(
            "font", "abel.ttf"), int(self.unit*2.3))

        self.sprites = []
        self.sprites.append(
            FoodBlock(self.unit*2, (4, 1), FoodBlockKind.APPLE))
        self.sprites.append(FoodBlock(self.unit*2, (4, 3), FoodBlockKind.GOLD))

    @property
    def elapse(self):
        return "%02d:%02d" % (int(self.seconds/60), self.seconds % 60)

    def add_second(self):
        self.seconds += 1

    def set_length(self, length):
        self.length = length

    def add_score(self, score):
        self.score += score

    def update(self):

        self.image.fill((50, 50, 50))

        lines = [str(self.score), self.elapse]

        for ii in range(len(lines)):
            text = lines[ii]
            sprite = self.sprites[ii]
            text = self.font.render(text, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.right = self.image.get_rect().right-int(self.unit*4)
            textRect.y = int(self.unit*(ii*4+1.6))
            self.image.blit(text, textRect)
            self.image.blit(sprite.image, sprite.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
