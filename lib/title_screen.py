#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame

# YASP common imports
import data
import util
from constants import Constants

# YASP imports
from highscores import Highscores
from sound_engine import MusicPlayer
from gui import MenuButton


class TitleScreen:
    def __init__(self, screen, unit, preferences):
        self.screen = screen
        self.unit = unit
        self.preferences = preferences
        self.running = True
        self.music_player = MusicPlayer("title")
        self.clock = pygame.time.Clock()
        self.choice = 0
        self.size = self.screen.get_size()

        self.img_title = pygame.image.load(data.filepath("title", "title.png"))
        self.img_credits = pygame.image.load(
            data.filepath("title", "credits.png"))
        self.img_background = pygame.image.load(
            data.filepath("title", "background.jpg"))
        self.img_background = pygame.transform.smoothscale(
            self.img_background, util.scale(self.img_background,
                                            width=self.size[0]))
        self.img_background.set_alpha(50)
        self.img_background_rect = self.img_background.get_rect()
        self.img_background_rect.centerx = self.screen.get_rect().centerx
        self.img_background_rect.centery = self.screen.get_rect().centery

    def draw_background(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img_background, self.img_background_rect)

    def main(self):
        self.music_player.play()

        img_title = pygame.transform.smoothscale(
            self.img_title, util.scale(self.img_title, width=self.unit*35))
        img_title_rect = img_title.get_rect()
        img_title_rect.centerx = self.screen.get_rect().centerx
        img_title_rect.y = self.unit*3

        self.choice = 0
        start_game = False

        btn_play = MenuButton("PLAY", self.unit, (self.unit*17, self.unit*3))
        btn_play.rect.centerx = self.screen.get_rect().centerx
        btn_play.rect.y = self.unit*29
        btn_play.set_status(1)

        btn_highscores = MenuButton(
            "HIGH SCORES", self.unit, (self.unit*17, self.unit*3))
        btn_highscores.rect.centerx = self.screen.get_rect().centerx
        btn_highscores.rect.y = self.unit*33

        btn_fullscreen = MenuButton(["FULLSCREEN", "WINDOWED"][self.preferences.get(
            'fullscreen')], self.unit, (self.unit*17, self.unit*3))
        btn_fullscreen.rect.centerx = self.screen.get_rect().centerx
        btn_fullscreen.rect.y = self.unit*37

        btn_credits = MenuButton("CREDITS", self.unit,
                                 (self.unit*17, self.unit*3))
        btn_credits.rect.centerx = self.screen.get_rect().centerx
        btn_credits.rect.y = self.unit*41

        btn_exit = MenuButton("QUIT", self.unit, (self.unit*17, self.unit*3))
        btn_exit.rect.centerx = self.screen.get_rect().centerx
        btn_exit.rect.y = self.unit*45
        buttons = pygame.sprite.Group()
        buttons.add([btn_play, btn_fullscreen,
                     btn_highscores, btn_credits, btn_exit])

        # dbg = util.debugBackground(self.size, self.unit)
        self.draw_background()

        last_choice = -1

        while not start_game:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.choice -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.choice += 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.choice == 0:
                            start_game = True
                        elif self.choice == 1:
                            self.highscores()
                            self.draw_background()
                        elif self.choice == 2:
                            # return to MAIN.PY to save prefs and apply fullscreen mode
                            self.preferences.set(
                                'fullscreen', not self.preferences.get('fullscreen'))
                            return
                        elif self.choice == 3:
                            self.credits()
                            self.draw_background()
                        else:
                            self.running = False
                            return
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        return
                    elif event.key == pygame.K_1:
                        pygame.image.save(self.screen, "screenshot.jpg")
                elif event.type == pygame.QUIT:
                    self.running = False
                    return
            if self.choice != last_choice:
                if self.choice < 0:
                    self.choice = 4
                elif self.choice > 4:
                    self.choice = 0
                btn_play.set_status(0)
                btn_highscores.set_status(0)
                btn_fullscreen.set_status(0)
                btn_credits.set_status(0)
                btn_exit.set_status(0)
                if self.choice == 0:
                    btn_play.set_status(1)
                elif self.choice == 1:
                    btn_highscores.set_status(1)
                elif self.choice == 2:
                    btn_fullscreen.set_status(1)
                elif self.choice == 3:
                    btn_credits.set_status(1)
                elif self.choice == 4:
                    btn_exit.set_status(1)
                last_choice = self.choice

            buttons.update()
            self.screen.blit(img_title, img_title_rect)
            buttons.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)
        self.music_player.stop()

    def highscores(self, scored=False):
        #scored = {'elapse':str,'score':int,'index':int,'scored':bool}

        back = False

        btn_back = MenuButton("BACK", self.unit, (self.unit*17, self.unit*3))
        btn_back.rect.centerx = self.screen.get_rect().centerx
        btn_back.rect.y = self.unit*45
        btn_back.set_status(1)

        self.draw_background()

        highscores = Highscores()
        if scored and not scored['scored']:
            highscores.insert("Your name", str(
                scored["score"]), scored["elapse"])

        box = pygame.Surface((self.size[1], self.size[1]))
        box.fill((255, 255, 255))
        box.set_alpha(150)
        box_rect = box.get_rect()
        box_rect.centerx = self.screen.get_rect().centerx
        box_rect.y = 0
        self.screen.blit(box, box_rect)

        font_text = pygame.font.Font(data.filepath(
            "font", "abel.ttf"), int(self.unit * 1.6))
        font_title = pygame.font.Font(data.filepath(
            "font", "abel.ttf"), int(self.unit * 5))
        color_text = (30, 30, 30)
        color_title = (122, 30, 30)

        posy = 8*self.unit
        advance = int(2.2*self.unit)

        btn_back.update()
        self.screen.blit(btn_back.image, btn_back.rect)

        title = font_title.render("HIGH SCORES", True, color_title)
        rect = title.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.y = 1*self.unit

        self.screen.blit(title, rect)
        line = pygame.Surface((self.size[1], int(self.unit*2.2)))
        line.fill((255, 255, 255))
        line.set_alpha(50)
        line_rect = line.get_rect()
        line_rect.centerx = self.screen.get_rect().centerx
        line_me = pygame.Surface((self.size[1], int(self.unit*2.2)))
        line_me.fill((30, 200, 30))
        line_me.set_alpha(50)
        ii = 0
        for el in highscores.scores:
            index = font_text.render(str(ii+1), True, color_title)
            name = font_text.render(el["name"], True, color_text)
            elapse = font_text.render(el["elapse"], True, color_text)
            score = font_text.render(el["score"], True, color_text)
            line_rect.y = posy
            if not ii % 2:
                self.screen.blit(line, line_rect)
            if scored and scored["scored"] and ii == scored["index"] or ii == Constants.MAXSCORE:
                self.screen.blit(line_me, line_rect)
            rect = index.get_rect()
            rect.y = posy

            rect.x = self.screen.get_rect().centerx-self.unit*13
            if ii < Constants.MAXSCORE:
                self.screen.blit(index, rect)
            rect.x += self.unit*3
            self.screen.blit(name, rect)
            rect.x += self.unit*16
            self.screen.blit(elapse, rect)
            rect.x += self.unit*5
            self.screen.blit(score, rect)
            posy += advance
            ii += 1

        while not back:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_1:
                        pygame.image.save(self.screen, "screenshot.jpg")
                elif event.type == pygame.QUIT:
                    self.running = False
                    return

            btn_back.update()
            btn_back.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)

    def credits(self):
        img_credits = pygame.transform.smoothscale(
            self.img_credits, util.scale(self.img_credits, height=self.unit*13))
        img_credits_rect = img_credits.get_rect()
        img_credits_rect.centerx = self.screen.get_rect().centerx
        img_credits_rect.y = self.unit*2

        back = False

        btn_back = MenuButton("BACK", self.unit, (self.unit*17, self.unit*3))
        btn_back.rect.centerx = self.screen.get_rect().centerx
        btn_back.rect.y = self.unit*45
        btn_back.set_status(1)

        self.draw_background()

        box = pygame.Surface((self.size[1], self.size[1]))
        box.fill((255, 255, 255))
        box.set_alpha(150)
        box_rect = box.get_rect()
        box_rect.centerx = self.screen.get_rect().centerx
        box_rect.y = 0
        self.screen.blit(box, box_rect)

        font = pygame.font.Font(data.filepath(
            "font", "abel.ttf"), int(self.unit * 1.5))
        color_text = (30, 30, 30)
        color_title = (122, 30, 30)

        credits = Constants.CREDITS.split("\n")
        spooler = []
        for line in credits:
            color = color_text
            if line and line[0] == "*":
                line = line[1:]
                color = color_title
            spooler.append(font.render(line, True, color))

        posy = 16*self.unit
        advance = int(1.6*self.unit)

        self.screen.blit(img_credits, img_credits_rect)
        btn_back.update()
        btn_back.draw(self.screen)

        for el in spooler:
            rect = el.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.y = posy
            self.screen.blit(el, rect)
            posy += advance

        while not back:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_1:
                        pygame.image.save(self.screen, "screenshot.jpg")
                elif event.type == pygame.QUIT:
                    self.running = False
                    return

            pygame.display.flip()
            self.clock.tick(30)
