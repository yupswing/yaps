#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

# #TODO I NEED TO DELETE THIS FILE AND MERGE THESE FUNCTIONS IN THE CLASSES

# Python imports
import pygame
import math


def center(surface, obj):
    osize = obj.get_size()
    ssize = surface.get_size()
    x = int(ssize[0] / 2) - int(osize[0] / 2)
    y = int(ssize[1] / 2) - int(osize[1] / 2)
    return (x, y)


def scale(obj, factor=0, height=0, width=0):
    w, h = obj.get_size()

    if factor:
        w, h = (int(w*factor), int(h*factor))
    elif height:
        w = int((height/float(h))*w)
        h = height
    elif width:
        h = int((width/float(w))*h)
        w = width

    return (w, h)


def collide(unit, group, position):
    el = pygame.sprite.Sprite()
    el.rect = pygame.Rect(position[0]*unit, position[1]*unit, unit, unit)
    return pygame.sprite.spritecollide(el, group, False)


def points_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dist = dx**2 + dy**2
    return math.sqrt(dist)


def coord2pos(unit, coord):
    return [int(coord[0]/unit), int(coord[1]/unit)]


def pos2coord(unit, pos):
    return [pos[0]*unit, pos[1]*unit]


def extractcoord(unit, group):
    coords = []
    for el in group:
        coords.append(coord2pos(unit, [el.rect.x, el.rect.y]))
    return coords


def debugBackground(size, unit):
    colors = [(255, 255, 255), (212, 212, 212)]
    background = pygame.Surface(size)
    tile_width = unit
    width, height = size
    zerox = int((width/2) % unit)
    y = 0
    while y < height:
        x = int(zerox-unit*1.5)
        while x < width:
            row = y // tile_width
            col = x // tile_width
            pygame.draw.rect(
                background,
                colors[(row + col) % 2],
                pygame.Rect(x, y, tile_width, tile_width))
            x += tile_width
        y += tile_width
    return background
