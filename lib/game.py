#
#  YetAnotherPythonSnake 0.94
#  Author: Simone Cingano (simonecingano@gmail.com)
#  Web: http://simonecingano.it
#  Licence: MIT
#

import pygame
import random

# YASP common imports
import data
import util
from constants import Constants
from gui import InputBox, Label

# YASP imports
from sound_engine import SoundPlayer, MusicPlayer
from object_pavement import Pavement
from object_snake import Snake
from object_foods import Foods
from object_walls import Walls
from score import Score
from highscores import Highscores
from title_screen import TitleScreen


class Game:
    def __init__(self, screen, unit, preferences):
        self.screen = screen
        self.unit = unit
        self.preferences = preferences
        self.running = True

        self.sounds = SoundPlayer((
            ('fall', 'fall.wav'),
            ('ding', 'ding.wav'),
            ('eat', 'eat.wav'),
            ('move', 'move.wav'),
            ('splat', 'splat.wav')
        ))
        self.music = MusicPlayer("game")

        self.clock = pygame.time.Clock()
        self.tick = Constants.FPS

        self.size = Constants.UNITS*self.unit

        self.surface = pygame.Surface((self.size, self.size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.centerx = self.screen.get_rect().centerx
        self.surface_rect.centery = self.screen.get_rect().centery

        self.img_background = pygame.image.load(
            data.filepath("title", "background.jpg"))
        self.img_background = pygame.transform.smoothscale(self.img_background,
                                                           util.scale(self.img_background,
                                                                      width=self.screen.get_rect().width))
        self.img_background.set_alpha(30)
        self.img_background_rect = self.img_background.get_rect()
        self.img_background_rect.centerx = self.screen.get_rect().centerx
        self.img_background_rect.centery = self.screen.get_rect().centery

    def main(self):
        self.music.play()

        # Screen base
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img_background, self.img_background_rect)

        highscores = Highscores()

        # Main instances
        pavement = Pavement(self.unit)
        snake = Snake(self.unit)
        foods = Foods(self.unit)
        walls = Walls(self.unit)
        score = Score(self.unit, self.surface_rect)

        # first gold between 30 & 60 seconds
        nextgold = random.randint(*Constants.TIMERANGE_GOLD) * Constants.FPS
        makegold = False
        # first gold between 30 & 60 seconds
        nextwall = random.randint(*Constants.TIMERANGE_WALL) * Constants.FPS
        makewall = False

        updatestats = True

        counter = 0

        flag_music = True
        flag_pause = False
        # MAIN LOOP
        while self.running:
            # time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    elif event.key == pygame.K_m:
                        flag_music = not flag_music
                        if flag_music:
                            self.music.play()
                        else:
                            self.music.stop()

                    elif event.key == pygame.K_1:
                        pygame.image.save(self.screen, "screenshot.jpg")

                    elif event.key == pygame.K_SPACE or event.key == pygame.K_p:
                        flag_pause = True
                        self.print_text("PAUSE")
                        while flag_pause:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                                        flag_pause = False

                    else:
                        # Time to change direction
                        action = 0
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            action = 1
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            action = 2
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            action = 3
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            action = 4
                        if action:
                            self.sounds.play("move")
                            snake.action(action)

            # Snake movements and pavement reactions
            snake.move()
            pavement.passage(snake.head)
            pavement.make_regrow(snake.tail)

            # Snake has eaten?
            if foods.check(snake.head):
                updatestats = True
                snake.grow(Constants.GROW)
                score.add_score(foods.score)
                self.sounds.play("eat")

            # Snake
            if walls.check(snake.head):
                snake.is_alive = False

            # Snake is dead?
            if not snake.is_alive:
                # blood splash (bin on head, little on body)
                pavement.bloodsplat(snake.head)
                [pavement.bloodsplat(x, 1)
                 for x in snake.body if random.randint(0, 2) == 0]
                # redraw all the snake
                snake.set_dirty(1)
                self.sounds.play("splat")
                self.running = False

            # Gold generator (After pseudo-random time a golden apple will appear)
            nextgold -= 1
            if nextgold < 0:
                makegold = True
                nextgold = random.randint(
                    *Constants.TIMERANGE_GOLD)*Constants.FPS

            # Wall generator (After pseudo-random time a wall will appear)
            nextwall -= 1
            if nextwall < 0:
                makewall = True
                nextwall = random.randint(
                    *Constants.TIMERANGE_WALL)*Constants.FPS

            # Foods request to create an apple
            # Game has to provide to Foods the list of forbidden blocks
            if foods.needapple or makegold or makewall:
                forbidden = [[-1, -1]]
                forbidden.extend(foods.get_forbidden())
                forbidden.extend(snake.get_forbidden())
                forbidden.extend(walls.get_forbidden())

                # Creates the apples and make the pavement Grass
                if foods.needapple:
                    newpos = foods.make_apple(forbidden)
                    pavement.make_grass(newpos)
                    forbidden.extend(newpos)
                if makegold:
                    self.sounds.play('ding')
                    newpos = foods.make_gold(forbidden)
                    pavement.make_grass(newpos)
                    forbidden.extend(newpos)
                    makegold = False
                if makewall:
                    self.sounds.play('fall')
                    newpos = walls.make_solid(forbidden)
                    pavement.make_none(newpos)
                    forbidden.extend(newpos)
                    makewall = False

            # Foods request pavement update
            for pos in foods.refresh:
                pavement.passage(pos)
                foods.refresh.remove(pos)
                del pos

            # Updates and draws
            pavement.update()
            pavement.draw(self.surface)
            walls.update()
            walls.draw(self.surface)
            snake.update()
            snake.draw(self.surface)
            foods.update()
            foods.draw(self.surface)

            if updatestats or not counter % Constants.FPS:
                score.set_length(snake.length)
                score.update()
                score.draw(self.screen)
                updatestats = False

            if not counter % Constants.FPS:
                score.add_second()
                counter = 0

            # Surface on surface... weeee!
            self.screen.blit(self.surface, self.surface_rect)

            pygame.display.update()
            self.clock.tick(self.tick)
            counter += 1
            # END OF MAIN LOOP

        if not snake.is_alive:

            self.print_text("GAME OVER")

            if highscores.check(score.score, score.elapse):
                current_string = ''
                complete = False

                inputbox = InputBox(self.unit)
                inputbox.rect.centerx = self.screen.get_rect().centerx
                inputbox.rect.centery = self.screen.get_rect().centery
                inputbox.draw(self.screen)

                pygame.display.update()
                pygame.event.clear()
                redraw = False
                while not complete:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        return
                    if event.type != pygame.KEYDOWN:
                        continue
                    if event.key == pygame.K_BACKSPACE:
                        current_string = current_string[:-1]
                        redraw = True
                    elif event.key == pygame.K_RETURN:
                        if len(current_string) == 0:
                            current_string = 'Mysterious player'
                        complete = True
                    elif event.unicode:
                        if len(current_string) <= 15:
                            c = ord(event.unicode)
                            if c >= 32 and c <= 126 or c == 8:
                                current_string += event.unicode
                                redraw = True
                    if redraw:
                        redraw = False
                        inputbox.set_text(current_string)
                        inputbox.update()
                        inputbox.draw(self.screen)
                        pygame.display.update()
                position = highscores.insert(
                    current_string, score.score, score.elapse)
                highscores.save()
                scored = {'index': position, 'scored': True}
            else:
                counter = Constants.FPS*3  # 3 seconds
                pygame.display.update()
                while counter > 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                            counter = 0
                    self.clock.tick(self.tick)
                    pygame.display.update()
                    counter -= 1

                scored = {'elapse': score.elapse,
                          'score': score.score, 'scored': False}

            ts = TitleScreen(self.screen, self.unit, self.preferences)
            ts.highscores(scored)
            del ts

        self.music.stop()
        return

    def print_text(self, text):
        label = Label(self.unit, text, int(self.unit*10), (255, 255, 255))
        label.rect.centerx = self.screen.get_rect().centerx
        label.rect.y = self.unit*5
        label.draw(self.screen)
        label.set_fontsize(self.unit*11)
        label.set_fontcolor((140, 20, 10))
        label.rect.centerx = self.screen.get_rect().centerx
        label.update()
        label.draw(self.screen)
        del label
        pygame.display.update()
