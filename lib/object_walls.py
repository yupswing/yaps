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


class WallBlockKind:
    SOLID = 0


class Walls(object):

    def __init__(self, unit):
        self.unit = unit
        self.group = pygame.sprite.LayeredDirty()

    def get_forbidden(self):
        return util.extractcoord(self.unit, self.group)

    def make_solid(self, forbidden):
        return self.make(WallBlockKind.SOLID, forbidden)

    def make(self, kind, forbidden):
        position = [-1, -1]
        while position in forbidden:
            position = [random.randint(
                0, Constants.UNITS-1), random.randint(0, Constants.UNITS-1)]
        self.group.add(WallBlock(self.unit, position, kind))
        return position

    def check(self, position):
        sprites = util.collide(self.unit, self.group, position)
        for el in sprites:
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


class WallBlock(pygame.sprite.DirtySprite):
    image = None

    def __init__(self, unit, position, kind):
        pygame.sprite.DirtySprite.__init__(self)
        self.unit = unit
        self.kind = kind
        self.image = pygame.Surface((self.unit, self.unit))
        self.image.set_colorkey(Constants.ALPHA)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*self.unit
        self.rect.y = position[1]*self.unit

        if self.kind == WallBlockKind.SOLID:
            color = (0, 0, 0)
            color2 = (100, 100, 100)
            self.is_alive = -1  # forever

        self.layer = 10
        self.dirty = 1

        self.image.fill(Constants.ALPHA)
        size = int(self.unit*0.3)
        offset = int((self.unit-size)/2)+1
        pygame.draw.rect(self.image, color, (0, 0, self.unit, self.unit), 0)
        pygame.draw.rect(self.image, color2, (offset, offset, size, size), 0)

    def update(self):
        if self.is_alive > 0:
            self.is_alive -= 1
