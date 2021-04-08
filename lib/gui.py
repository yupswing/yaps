#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame

# YASP common imports
import data


class GuiObject(pygame.sprite.DirtySprite):

    def __init__(self, unit, size=(0, 0), dirty=2):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.surface.Surface(size)
        self.rect = pygame.rect.Rect((0, 0), (0, 0))

        self.unit = unit
        self.size = size
        self.rect = self.image.get_rect()

        self._valid = False
        self.dirty = dirty

    def invalidate(self):
        self._valid = False

    def get_size(self):
        return self.size

    def render(self):
        if not self.dirty == 2:
            self.dirty = 1
        self._valid = True

    def update(self):
        if not self._valid:
            self.render()

    def draw(self, surface):
        if self.dirty == 0:
            return
        if self.dirty == 1:
            self.dirty = 0
        surface.blit(self.image, self.rect)


class MenuButton(GuiObject):

    def __init__(self, text, unit, size, dirty=1):

        GuiObject.__init__(self, unit, size, dirty)

        self.text = text
        self.status = 0

        self.text = text
        self.label = Label(self.unit, self.text, int(
            self.unit*2), (255, 255, 255), dirty=2)
        self.label.rect.centerx = self.rect.centerx
        self.label.rect.centery = self.rect.centery

        self.update()

    def set_status(self, status):
        if status == self.status:
            return
        self.status = status
        self.invalidate()

    def render(self):
        color = (5, 113, 10)
        if self.status == 1:
            color = (255, 255, 255)
        self.image.fill((0, 0, 0))
        border = int(self.unit / 3)
        pygame.draw.rect(self.image, color, (0, 0, self.size[0], border), 0)
        pygame.draw.rect(self.image, color, (0, 0, border, self.size[1]), 0)
        pygame.draw.rect(self.image, color,
                         (self.size[0]-border, 0, border, self.size[1]), 0)
        pygame.draw.rect(self.image, color,
                         (0, self.size[1]-border, self.size[0], border), 0)
        self.label.draw(self.image)

        GuiObject.render(self)

    def update(self):
        GuiObject.update(self)


class Label(GuiObject):

    def __init__(self, unit, text, fontsize, fontcolor, dirty=1):

        size = (0, 0)
        GuiObject.__init__(self, unit, size, dirty)

        self.text = text
        self.fontcolor = fontcolor
        self.set_fontsize(fontsize)

        self.update()

    def set_text(self, text):
        self.text = text
        self.invalidate()

    def set_fontcolor(self, fontcolor):
        self.fontcolor = fontcolor
        self.invalidate()

    def set_fontsize(self, fontsize):
        self.font = pygame.font.Font(
            data.filepath("font", "abel.ttf"), fontsize)
        self.fontsize = fontsize
        self.invalidate()
        self.render()  # size updated

    def set_position(self, rect):
        self.rect = rect
        self.invalidate()

    def render(self):

        self.image = self.font.render(self.text, True, self.fontcolor)
        rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y

        GuiObject.render(self)

    def update(self):
        GuiObject.update(self)


class InputBox(GuiObject):

    def __init__(self, unit, label="", text="", dirty=1):
        size = (unit*17, unit*6)
        GuiObject.__init__(self, unit, size, dirty=1)

        self.font = pygame.font.Font(data.filepath(
            "font", "abel.ttf"), int(self.unit * 2))
        self.text = text

        self.label = Label(self.unit, "Digit your name and press ENTER", int(
            self.unit*1.3), (255, 255, 255), dirty=2)
        self.label.rect.centery = int(self.rect.centery / 2)
        self.label.rect.centerx = self.rect.centerx

        self.update()

    def set_text(self, text):
        self.text = text
        self.invalidate()

    def update(self):
        # other here
        GuiObject.update(self)

    def render(self):
        color = (5, 113, 10)
        self.image.fill((50, 50, 50))

        size = (self.unit*17, self.unit*3)
        temp = pygame.Surface(size)
        temp_rect = temp.get_rect()
        temp_rect.x = 0
        temp_rect.y = self.unit*3
        temp.fill((0, 0, 0))

        text_image = self.font.render(self.text+"_", True, (255, 255, 255))
        text_image_rect = text_image.get_rect()
        text_image_rect.x = self.unit
        text_image_rect.centery = temp.get_rect().centery

        border = int(self.unit / 3)
        pygame.draw.rect(temp, color, (0, 0, size[0], border), 0)
        pygame.draw.rect(temp, color, (0, 0, border, size[1]), 0)
        pygame.draw.rect(temp, color, (size[0]-border, 0, border, size[1]), 0)
        pygame.draw.rect(temp, color, (0, size[1]-border, size[0], border), 0)

        temp.blit(text_image, text_image_rect)
        self.image.blit(temp, temp_rect)
        self.label.draw(self.image)

        GuiObject.render(self)
