#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame

# YASP common imports
import util
from constants import Constants


class SnakeBlockKind:
    HEAD = 0
    BODY = 1


class SnakeBlockOrientation:
    N = 0
    S = 1
    W = 2
    E = 3


class Snake(object):

    def __init__(self, unit):
        self.unit = unit
        self.is_alive = True

        # Initial orientation
        self.vx = 0
        self.vy = -1
        self.orientation = SnakeBlockOrientation.N

        self.growmore = Constants.START_LENGTH

        self.movelock = False  # prevent double move between clock

        self.head = None  # head block position
        self.tail = None  # removed block position

        self.length = 0
        self.body = []          # sprites coordinates
        self.body_sprites = []  # sprites
        self.addBody((int(0.5*Constants.UNITS), int(0.5*Constants.UNITS)))

    def get_forbidden(self):
        return util.extractcoord(self.unit, self.body_sprites)

    def addBody(self, position):
        if self.length > 0:
            self.body_sprites[0].b_orientation = self.orientation
            self.body_sprites[0].update_kind(SnakeBlockKind.BODY)
        b = SnakeBlock(self.unit, position,
                       SnakeBlockKind.HEAD, self.orientation)
        self.body.insert(0, position)
        self.body_sprites.insert(0, b)
        self.head = position

    def removeBody(self):
        x = self.body_sprites.pop()
        self.tail = self.body.pop()
        del x

    def update(self):
        for el in self.body_sprites:
            el.update()

    def set_dirty(self, dirty):
        for el in self.body_sprites:
            el.dirty = dirty

    def draw(self, surface):
        for el in self.body_sprites:
            if el.dirty == 2 or el.dirty == 1:
                surface.blit(el.image, el.rect)
                if el.dirty == 1:
                    el.dirty = 0

    def action(self, movement):
        if self.movelock:
            return
        """ Handle keyboard events. """
        if movement == 1:
            if self.vy == 1:
                return
            self.orientation = SnakeBlockOrientation.N
            self.vx = 0
            self.vy = -1
        elif movement == 2:
            if self.vy == -1:
                return
            self.orientation = SnakeBlockOrientation.S
            self.vx = 0
            self.vy = 1
        elif movement == 3:
            if self.vx == 1:
                return
            self.orientation = SnakeBlockOrientation.W
            self.vx = -1
            self.vy = 0
        elif movement == 4:
            if self.vx == -1:
                return
            self.orientation = SnakeBlockOrientation.E
            self.vx = 1
            self.vy = 0
        self.movelock = True

    def get_x(self, index=0):
        return self.body[index][0]

    def get_y(self, index=0):
        return self.body[index][1]

    def grow(self, size=1):
        self.growmore += size

    def move(self):
        next = [self.get_x()+self.vx, self.get_y()+self.vy]

        if next in self.body:
            self.is_alive = False

        # exit left, appear right and so on
        if next[0] < 0:
            next[0] = Constants.UNITS-1
        if next[0] > Constants.UNITS-1:
            next[0] = 0
        if next[1] < 0:
            next[1] = Constants.UNITS-1
        if next[1] > Constants.UNITS-1:
            next[1] = 0

        self.addBody(next)

        if self.growmore:
            self.growmore -= 1
            self.length += 1
        else:
            self.removeBody()

        self.movelock = False  # reset flag


class SnakeBlock(pygame.sprite.DirtySprite):
    image = None

    def __init__(self, unit, position, kind, orientation):
        pygame.sprite.DirtySprite.__init__(self)
        self.unit = unit
        self.image = pygame.Surface((self.unit, self.unit))
        self.image.set_colorkey(Constants.ALPHA)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*self.unit
        self.rect.y = position[1]*self.unit
        self.orientation = orientation
        self.b_orientation = None
        self.dirty = 1
        self.layer = 10
        self.update_kind(kind)

    def update_kind(self, kind):
        self.kind = kind
        self.dirty = 1

        if self.kind == SnakeBlockKind.HEAD:
            color = (4, 80, 7)
            color2 = (200, 200, 200)
        elif self.kind == SnakeBlockKind.BODY:
            color = (5, 113, 10)
            color2 = (3, 69, 6)

        size = int(self.unit*0.7)+1
        pos = int((self.unit-size)/2)
        offset = self.unit-size

        size_c = int(self.unit*0.3)+1
        pos_c = int((self.unit-size)/2)
        offset_c = self.unit-size

        rect_a = pygame.Rect(pos, pos, size, size)
        rect_b = pygame.Rect(pos, pos, size, size)
        rect_c = pygame.Rect(pos_c, pos_c, size_c, size_c)
        if self.orientation == SnakeBlockOrientation.N:
            rect_a.y = offset
            rect_c.y = offset_c
        elif self.orientation == SnakeBlockOrientation.S:
            rect_a.y = 0
            rect_c.y = 0
        elif self.orientation == SnakeBlockOrientation.E:
            rect_a.x = 0
            rect_c.x = 0
        elif self.orientation == SnakeBlockOrientation.W:
            rect_a.x = offset
            rect_c.x = offset_c

        if self.b_orientation == SnakeBlockOrientation.N:
            rect_b.y = 0
        elif self.b_orientation == SnakeBlockOrientation.S:
            rect_b.y = offset
        elif self.b_orientation == SnakeBlockOrientation.E:
            rect_b.x = offset
        elif self.b_orientation == SnakeBlockOrientation.W:
            rect_b.x = 0

        self.image.fill(Constants.ALPHA)
        pygame.draw.rect(self.image, color, rect_a)
        pygame.draw.rect(self.image, color, rect_b)
        pygame.draw.rect(self.image, color2, rect_c)
