#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame
import random

# YASP common imports
import util
from constants import Constants


class FoodBlockKind:
    APPLE = 0
    GOLD = 1


class Foods(object):

    def __init__(self, unit):
        self.unit = unit
        self.group = pygame.sprite.LayeredDirty()
        self.needapple = True
        self.score = 0
        self.refresh = []

    def get_forbidden(self):
        return util.extractcoord(self.unit, self.group)

    def make_apple(self, forbidden):
        return self.make(FoodBlockKind.APPLE, forbidden)

    def make_gold(self, forbidden):
        return self.make(FoodBlockKind.GOLD, forbidden)

    def make(self, kind, forbidden):
        self.needapple = False
        position = [-1, -1]
        while position in forbidden:
            position = [random.randint(
                0, Constants.UNITS-1), random.randint(0, Constants.UNITS-1)]
        self.group.add(FoodBlock(self.unit, position, kind))
        return position

    def check(self, position):
        sprites = util.collide(self.unit, self.group, position)
        for el in sprites:
            if el.kind == FoodBlockKind.APPLE:
                self.needapple = True
            self.group.remove(el)
            self.score = el.score
            del el
            return True
        return False

    def update(self):
        self.group.update()
        for el in self.group:
            if el.is_alive == 0:
                self.group.remove(el)
                self.refresh.append(util.coord2pos(
                    self.unit, [el.rect.x, el.rect.y]))
                del el

    def draw(self, surface):
        self.group.draw(surface)


class FoodBlock(pygame.sprite.DirtySprite):
    image = None

    def __init__(self, unit, position, kind):
        # self.dirty = 0 means no repainting
        #              1 repaint and set to 0
        #              2 repaint every frame
        pygame.sprite.DirtySprite.__init__(self)
        self.unit = unit
        self.kind = kind
        self.image = pygame.Surface((self.unit, self.unit))
        self.image.set_colorkey(Constants.ALPHA)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*self.unit
        self.rect.y = position[1]*self.unit

        if self.kind == FoodBlockKind.APPLE:
            color = (184, 11, 8)
            color2 = (5, 113, 10)
            self.score = 1
            self.is_alive = -1  # forever
        elif self.kind == FoodBlockKind.GOLD:
            color = (30, 106, 140)
            color2 = (244, 214, 53)
            self.score = 5
            self.is_alive = Constants.FPS * 5  # 5 seconds

        self.layer = 10
        self.dirty = 2

        self.image.fill(Constants.ALPHA)
        size = int(self.unit*0.8) + 1
        offset = int((self.unit-size)/2)+1
        pygame.draw.rect(self.image, color, (offset, offset, size, size), 0)
        pygame.draw.rect(self.image, color2, (offset*2,
                                              0, int(size/3), int(size/2)), 0)

    def update(self):
        if self.is_alive > 0:
            self.is_alive -= 1
