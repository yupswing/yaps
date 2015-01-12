#
#  YetAnotherPythonSnake 0.92
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://imente.it
#  Licence: (CC) BY-NC 3.0 [http://creativecommons.org/licenses/by-nc/3.0/]
#

import pygame
import random

#YASP common imports
import data
import util
from constants import Constants

class PavementBlockStatus:
    NONE=0
    GRASS=1
    FLAT=2
    REGROW=3
    BLOOD=4

class Pavement(object):

    def __init__(self, unit):
        self.unit = unit
        self.group = pygame.sprite.LayeredDirty()
        self._grid = []
        for x in range(Constants.UNITS):
            self._grid.append([])
            for y in range(Constants.UNITS):
                pavement = PavementBlock(self.unit,PavementBlockStatus.GRASS,(x,y))
                self.group.add(pavement)
                self._grid[x].append(pavement)

    def getByPosition(self,x,y):
        """ Get a sprite from coordinates """
        return self._grid[x][y]

    def passage(self,position):
        block = self.getByPosition(*position)
        block.refill = 0
        block.dirty = 1

    def make(self,position,kind):
        if not position: return
        self.getByPosition(*position).update_status(kind)

    def make_none(self,position):
        self.make(position,PavementBlockStatus.NONE)

    def make_grass(self,position):
        self.make(position,PavementBlockStatus.GRASS)

    def make_flat(self,position):
        self.make(position,PavementBlockStatus.FLAT)

    def make_regrow(self, position):
        self.make_flat(position)
        self.make(position,PavementBlockStatus.REGROW)

    def update(self):
        self.group.update()

    def draw(self,surface):
        self.group.draw(surface)

    def bloodsplat(self,position,radius=5):
        """ Create a blood splash around a position """
        for x in range(position[0]-radius,position[0]+radius+1):
            for y in range(position[1]-radius,position[1]+radius+1):
                if x >= 0 and x < Constants.UNITS and y >= 0 and y < Constants.UNITS:
                    distance = int(util.points_distance(position[0],position[1],x,y))
                    if random.randint(0,distance*3)<radius:
                        self.getByPosition(x,y).update_status(PavementBlockStatus.BLOOD)

class PavementBlock(pygame.sprite.DirtySprite):
    image = None

    def __init__(self, unit, status, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.unit = unit
        self.image = pygame.Surface((self.unit,self.unit))
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]*self.unit
        self.rect.y = position[1]*self.unit
        self.dirty = 1
        self.layer = 20
        self.refill = 0
        self.update_status(status)

    def update_status(self,status):
        if status == PavementBlockStatus.BLOOD and self.status == PavementBlockStatus.BLOOD: return
        self.status = status
        self.dirty = 1
        self.refill = 0
        if self.status == PavementBlockStatus.NONE:
            self.image.fill((0,0,0))
            self.dirty = 0 # no need to paint
        elif self.status == PavementBlockStatus.FLAT:
            move = random.randint(-20,+20)
            color_base = (200+move,150+move,120+move)
            self.image.fill(color_base)
        elif self.status == PavementBlockStatus.REGROW:
            # After the refill it will become GRASS
            self.refill = Constants.FPS * (2 + random.randint(-1,1)) # between 1 and 3 seconds 
        elif self.status == PavementBlockStatus.BLOOD:
            color_base = (140+random.randint(-50,50),20,10)
            self.image.fill(color_base)
            size = int(self.unit*0.3)

            draw = random.randint(-8,6)
            draw = int(draw / 2)

            size_a = int(size*(random.randint(0,20)/10.0))
            rect_a = pygame.Rect(int((random.randint(0,10)/10.0)*self.unit),int((random.randint(0,10)/10.0)*self.unit),size_a,size_a)
            size_b = int(size*(random.randint(0,20)/10.0))
            rect_b = pygame.Rect(int((random.randint(0,10)/10.0)*self.unit),int((random.randint(0,10)/10.0)*self.unit),size_b,size_b)
            size_c = int(size*(random.randint(0,20)/10.0))
            rect_c = pygame.Rect(int((random.randint(0,10)/10.0)*self.unit),int((random.randint(0,10)/10.0)*self.unit),size_c,size_c)
            pygame.draw.rect(self.image, (140+random.randint(-50,50),20,10), rect_a)
            pygame.draw.rect(self.image, (140+random.randint(-50,50),20,10), rect_b)
            pygame.draw.rect(self.image, (140+random.randint(-50,50),20,10), rect_c)
        elif self.status == PavementBlockStatus.GRASS:
            color_base = (110+random.randint(-50,50),220+random.randint(-50,30),35)
            self.image.fill(color_base)
            var = int(self.unit*0.1)

            draw = random.randint(-8,6)
            draw = int(draw / 2)

            for x in range(draw):
                color_line = (19,173+random.randint(-50,50),33)
                x1 = int(self.unit*0.5)+random.randint(-3*var,3*var)
                x2 = x1 + int(self.unit*0.1)+random.randint(-var,var)
                y1 = int(self.unit*0.8)+random.randint(-var,var)
                y2 = 0+random.randint(0,2*var)
                pygame.draw.aaline(self.image, color_line, (x1,y1),(x2,y2))

    def update(self):
        if self.status==PavementBlockStatus.REGROW:
            if self.refill>0: self.refill-=1
            if self.refill==1:
                    self.update_status(PavementBlockStatus.GRASS)
