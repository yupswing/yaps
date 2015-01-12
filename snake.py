#! /usr/bin/env python

import pygame
import random
import time,os

from cfontmanager import cFontManager

class Snake:
    def __init__(self, surface, grid, unit, mode, background_color):
        self.surface = surface
        self.vx = 0
        self.vy = -1

        self.alive = True
        self.growmore = 2*mode

        self.bodyerase = False

        self.newmove = False #prevent double move between clock
        self.grid = grid
        self.mode = mode
        self.unit = unit
        self.body_color = (5,113,10)
        self.body2_color = (3,69,6)
        self.head_color = (4,80,7)
        self.head2_color = (1,29,3)
        self.head3_color = (133,8,7)
        self.background_color = background_color
        self.body = [(int(grid/2),int(grid/2))]
        self.length = 1

    def action(self, movement):
        if self.newmove: return
        """ Handle keyboard events. """
        if movement==1:
            if self.vy == 1: return
            self.vx = 0
            self.vy = -1
        elif movement==2:
            if self.vy == -1: return
            self.vx = 0
            self.vy = 1
        elif movement==3:
            if self.vx == 1: return
            self.vx = -1
            self.vy = 0
        elif movement==4:
            if self.vx == -1: return
            self.vx = 1
            self.vy = 0
        self.newmove = True

    def getx(self,index=0):
        return self.body[index][0]

    def gety(self,index=0):
        return self.body[index][1]

    def grow(self,size=1):
        self.growmore+=size

    def move(self):
        next = (self.getx()+self.vx,self.gety()+self.vy)

        if next in self.body:
            self.alive = False

        if next[0] < 0 or next[0] >= self.grid:
            self.alive = False
        if next[1] < 0 or next[1] >= self.grid:
            self.alive = False

        self.body.insert(0,next)

        if self.growmore:
            self.bodyerase = False
            self.growmore-=1
            self.length+=1
        else:
            self.bodyerase = self.body[-1]
            self.body.pop()

        self.newmove = False #reset flag

    def draw(self):

        #the head
        size = self.unit
        pygame.draw.rect(self.surface, self.head_color, (grid2coord(self.getx(),self.unit,size), grid2coord(self.gety(),self.unit,size), size, size), 0)
        size = int(self.unit / 2) - 1
        pygame.draw.rect(self.surface, self.head2_color, (grid2coord(self.getx(),self.unit,size), grid2coord(self.gety(),self.unit,size), size, size), 0)
        # size = int(self.unit / 6)
        # pygame.draw.rect(self.surface, self.head3_color, (grid2coord(self.getx(),self.unit,size), grid2coord(self.gety(),self.unit,size), size, size), 0)
        #previous head become body
        size = self.unit
        pygame.draw.rect(self.surface, self.body_color, (grid2coord(self.getx(1),self.unit,size), grid2coord(self.gety(1),self.unit,size), size, size), 0)
        size = int(self.unit / 2) - 1
        pygame.draw.rect(self.surface, self.body2_color, (grid2coord(self.getx(1),self.unit,self.unit), grid2coord(self.gety(1),self.unit,self.unit), size, size), 0)

        #delete move body
        if self.bodyerase:
            size = self.unit
            pygame.draw.rect(self.surface, self.background_color, (grid2coord(self.bodyerase[0],self.unit,size), grid2coord(self.bodyerase[1],self.unit,size), size, size), 0)
            size = int(self.unit / 2) - 1
            pygame.draw.rect(self.surface, (60,60,60), (grid2coord(self.bodyerase[0],self.unit,size), grid2coord(self.bodyerase[1],self.unit,size), size, size), 0)

    def drawhead(self,x,y):
        size = int(self.unit / 2) - 1
        pygame.draw.rect(self.surface, self.head_color, (grid2coord(x,self.unit,size), grid2coord(y,self.unit,size), size, size), 0)
        size = int(self.unit / 4) - 1
        pygame.draw.rect(self.surface, self.head2_color, (grid2coord(x,self.unit,size), grid2coord(y,self.unit,size), size, size), 0)



#     def drawall(self):
        # size = self.unit
        # for el in self.body:
            # pygame.draw.rect(self.surface, self.body_color, (grid2coord(el[0],self.unit,size), grid2coord(el[1],self.unit,size), size, size), 0)
        # #the head
        # pygame.draw.rect(self.surface, self.head_color, (grid2coord(self.getx(),self.unit,size), grid2coord(self.gety(),self.unit,size), size, size), 0)

class Food:
    def __init__(self, surface, grid, unit, mode, forbidden=[]):
        self.surface = surface
        self.grid = grid
        self.unit = unit
        self.color = (184,11,8)
        self.color2 = (5,113,10)
        self.growpower = mode

        while 1:
            position = (random.randint(0, grid-1),random.randint(0, grid-1))
            if (not (position in forbidden)): break

        self.x = position[0]
        self.y = position[1]

    def draw(self,x=None,y=None):
        if x==None or y==None:
            x = self.x
            y = self.y
        size = int(self.unit / 2) + 1
        pygame.draw.rect(self.surface, self.color2, (grid2coord(x,self.unit,size), grid2coord(y,self.unit,self.unit), int(size/2),size), 0)

        pygame.draw.rect(self.surface, self.color, (grid2coord(x,self.unit,size), grid2coord(y,self.unit,size), size, size), 0)

def grid2coord(coord,unit,size):
    return coord*unit+int((unit-size)/2)+unit

class Game:
    def __init__(self):
        self.color_background = (50,50,50)

        # init
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        self.fontMgr = cFontManager(((os.path.join('data','abel.ttf'), 28),(os.path.join('data','abel.ttf'), 20)))


        self.snd_move = pygame.mixer.Sound('data/move.wav')
        self.snd_crash = pygame.mixer.Sound('data/crash.wav')
        self.snd_eat = pygame.mixer.Sound('data/eat.wav')
        self.snd_choose = pygame.mixer.Sound('data/choose.wav')

        self.height = int(pygame.display.Info().current_h*0.8)
        self.h = self.w = self.height

        self.img_title = pygame.image.load("data/snake.png")
        self.img_title = pygame.transform.smoothscale(self.img_title,(int(self.w*0.6),int((self.h*0.6)*0.66)))
        self.img_choose_difficult = pygame.image.load("data/choose-difficult.png")
        self.img_choose_difficult = pygame.transform.smoothscale(self.img_choose_difficult,(int(self.w*0.9),int((self.h*0.9)*0.25)))
        self.img_choose_grid = pygame.image.load("data/choose-grid.png")
        self.img_choose_grid = pygame.transform.smoothscale(self.img_choose_grid,(int(self.w*0.9),int((self.h*0.9)*0.25)))


        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()


    def drawbase(self,unit):
        self.screen.fill(self.color_background)
#boundaries
        pygame.draw.rect(self.screen, (0,0,0), (0,0, self.w, unit), 0)
        pygame.draw.rect(self.screen, (0,0,0), (0,0, unit, self.h), 0)
        pygame.draw.rect(self.screen, (0,0,0), (self.w-unit,0, unit, self.h), 0)
        pygame.draw.rect(self.screen, (0,0,0), (0,self.h-unit, self.w, unit), 0)

        rect = pygame.Rect(self.w-22*unit, self.h-unit, grid2coord(20,unit,unit), grid2coord(0,unit,unit))
        self.fontMgr.Draw(self.screen, os.path.join("data","abel.ttf"), 20, "YET ANOTHER PYTHON SNAKE v0.1 - Simone Cingano (CC) 2012 - http://imente.it", rect, (100, 100, 100), 'right', 'center', True)

    def _getUnit(self,grid):
        return int((self.w) / (grid+2)) # +2 are the borders

    def _resize(self,grid):
        #resize to compensate the module of size / grid
        self.h = self.w = self._getUnit(grid)*(grid+2)
        pygame.display.set_mode((self.w, self.h))

    def start(self):
        grid = 30
        unit = self._getUnit(grid)
        self._resize(grid)

        self.drawbase(unit)
        pygame.display.flip()
        exit = False

        pygame.mixer.music.load("data/background.mp3")
        pygame.mixer.music.play(-1)

        rect_title = self.img_title.get_rect()
        rect_title.center = (int(self.w*0.45),int(self.h*0.4))
        rect_info = self.img_choose_difficult.get_rect()
        rect_info.center = (int(self.w*0.5),int(self.h*0.8))

        mode = 0

        while not exit:
            choose = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        grid = 30
                        unit = self._getUnit(grid)
                        self.play(grid,2)
                        mode = 0
                        pygame.mixer.music.load("data/background.mp3")
                        pygame.mixer.music.play(-1)

                    if event.key == pygame.K_1:
                        choose = 1
                    if event.key == pygame.K_2:
                        choose = 2
                    if event.key == pygame.K_3:
                        choose = 3
                    elif event.key == pygame.K_ESCAPE:
                        if mode:
                            self.snd_choose.play()
                            mode = 0
                        else:
                            exit = True

                    if choose:
                        self.snd_choose.play()
                        if not mode:
                            mode = choose
                        else:
                            grid = [0,20,30,40][choose]
                            unit = self._getUnit(grid)
                            self.play(grid,mode)
                            mode = 0
                            pygame.mixer.music.load("data/background.mp3")
                            pygame.mixer.music.play(-1)


            size = int(unit / 2) - 1
            color = random.randint(30, 90)
            pygame.draw.rect(self.screen, (color,color,color), (grid2coord(random.randint(0, grid-1),unit,size), grid2coord(random.randint(0, grid-1),unit,size), size, size), 0)

            self.screen.blit(self.img_title, rect_title)
            if mode == 0:
                self.screen.blit(self.img_choose_difficult, rect_info)
            else:
                self.screen.blit(self.img_choose_grid, rect_info)
            pygame.display.flip()
            self.clock.tick(50)

    def play(self,grid,mode):
        self.h = self.w = self.height

        score = 0
        lastscore = -1
        tick = 5*mode
        seconds = 0

        length = 0
        lastlength = -1

        pygame.mixer.music.load("data/background-game.mp3")
        pygame.mixer.music.play(-1)

        unit = self._getUnit(grid)
        self._resize(grid)

        snake = Snake(self.screen, grid, unit, mode, self.color_background)
        food = Food(self.screen, grid, unit, mode)

        self.drawbase(unit)
        food.draw()
        pygame.display.flip()

        counter = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        action = 0
                        if event.key == pygame.K_UP: action = 1
                        elif event.key == pygame.K_DOWN: action = 2
                        elif event.key == pygame.K_LEFT: action = 3
                        elif event.key == pygame.K_RIGHT: action = 4
                        if action:
                            self.snd_move.play()
                            snake.action(action)

            snake.move()
            snake.draw()

            if food.x == snake.getx() and food.y == snake.gety():
                #eaten
                snake.grow(food.growpower)
                score+=1
                del food
                food = Food(self.screen,grid,unit,mode*2,snake.body)
                food.draw()
                self.snd_eat.play()

            if not snake.alive:
                self.snd_crash.play()
                running = False

            if lastscore != score or running == False:

                rect = pygame.Rect(grid2coord(0,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                pygame.draw.rect(self.screen, (0,0,0), rect)

                # rect = pygame.Rect(grid2coord(12,unit,unit), 0, grid2coord(5,unit,unit), grid2coord(0,unit,unit))
                # pygame.draw.rect(self.screen, (50,50,50), rect)

                lastscore = score
                food.draw(0,-1)
                rect = pygame.Rect(grid2coord(1,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                self.fontMgr.Draw(self.screen, os.path.join("data","abel.ttf"), 28, str(score), rect, (255, 255, 255), 'left', 'center', True)

            if lastlength != snake.length or running == False:

                rect = pygame.Rect(grid2coord(5,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                pygame.draw.rect(self.screen, (0,0,0), rect)

                lastlength = snake.length
                snake.drawhead(5,-1)
                rect = pygame.Rect(grid2coord(6,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                self.fontMgr.Draw(self.screen, os.path.join("data","abel.ttf"), 28, str(snake.length), rect, (255, 255, 255), 'left', 'center', True)

            if counter % tick == 0 or running == False:

                counter = 0
                seconds+=1
                rect = pygame.Rect(grid2coord(10,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                pygame.draw.rect(self.screen, (0,0,0), rect)
                
                size = int(unit / 2) - 1
                pygame.draw.rect(self.screen, (10,169,188), (grid2coord(10,unit,size), grid2coord(-1,unit,size), size, size), 0)

                rect = pygame.Rect(grid2coord(11,unit,unit), 0, grid2coord(4,unit,unit), grid2coord(0,unit,unit))
                timing = "%02d:%02d" % (int(seconds/60),seconds % 60)
                self.fontMgr.Draw(self.screen, os.path.join("data","abel.ttf"), 28, str(timing), rect, (255, 255, 255), 'left', 'center', True)


            pygame.display.flip()
            self.clock.tick(tick)
            counter+=1


thesnake = Game()
thesnake.start()
