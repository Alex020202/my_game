import pygame
import random
from Block import *
from Hero import *


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((320, 512 + 64))

        pygame.display.set_caption("Doodle Jump")

        self.background = pygame.image.load("../assets/pictures/background_s.png")
        self.bottom = pygame.image.load("../assets/pictures/Bottom.png")

        self.y_loc = 450  # position of spawning blocks
        self.r = 10  # Number of spawning blocks
        self.Blocks_list = []
        self.Blocks_list.append(Block(150, 501, False, self))
        for i in range(1, self.r):
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))
            self.y_loc -= random.randrange(50, 150)
        self.clock = pygame.time.Clock()
        self.move_details = 512 / 2 - 50  # line which character can't outstep
        self.Hero = Hero(self)
        self.count = 0  # player's score

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.textsurface = self.myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))

        self.music = 1  # number of playing music
        self.isRunning = True  # if main cycle is going

    def game_over(self):
        self.play_music(0)
        pygame.display.update()
        self.win.blit(self.background, (0, 0))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.win.blit(self.textsurface, (120, 100))
        self.textsurface = self.myfont.render('ХА-ХА-ХА'.format(int(self.count)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (120, 200))
        self.textsurface = self.myfont.render('ВЫ СЛИШКОМ ПЛОХО ИГРАЛИ!\n СЧЕТ:{}'.format(int(self.count)), False,
                                              (0, 0, 0))
        self.win.blit(self.textsurface, (0, 300))
        self.textsurface = self.myfont.render('СЧЕТ:{}'.format(int(self.count)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (120, 400))

    def play_music(self, key):
        self.key = key
        if self.key != 0:
            self.key = self.key % 5 + 1
        if self.key == 0 and self.music == 0:
            pygame.mixer.music.load("../assets/music/strashnye-zvuki-d-yavol-skiy-smeh.mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 1:
            pygame.mixer.music.load("../assets/music/coldplay_feat_beyonce_-_hymn_for_the_weekend_(zf.fm).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 2:
            pygame.mixer.music.load("../assets/music/Celldweller - Frozen.mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 3:
            pygame.mixer.music.load("../assets/music/teddybears_sthlm_and_mad_cobra_-_cobrastyle_(zaycev.net).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 4:
            pygame.mixer.music.load("../assets/music/ylvis_-_what_does_the_fox_say_(zaycev.net).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 5:
            pygame.mixer.music.load("../assets/music/tiesto__sevenn_-_boom_2017_(zf.fm).mp3")
            pygame.mixer.music.play()
            self.music += 1

    def draw_win(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.background, (0, 0))
        self.win.blit(self.bottom, (0, 511))
        self.textsurface = self.myfont.render('Score: {}'.format(int(self.count)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (0, 0))

        for i in range(self.r):
            self.Blocks_list[i].draw()
        self.Hero.draw()
        pygame.display.update()

    def run(self):
        while self.isRunning:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.Hero.x - self.Hero.speed + self.Hero.width > 0:
                    self.Hero.x -= self.Hero.speed
                    self.Hero.left = True
                    self.Hero.right = False
                else:
                    self.Hero.x = 320
            elif keys[pygame.K_RIGHT]:
                if self.Hero.x + self.Hero.speed < 320:
                    self.Hero.x += self.Hero.speed
                    self.Hero.left = False
                    self.Hero.right = True
                else:
                    self.Hero.x = 0
            else:
                self.Hero.left = False
                self.Hero.right = False
            if keys[pygame.K_SPACE]:
                self.Hero.isJump = True
                self.Hero.jumpcount = self.Hero.JumpHeight + 10
            if not self.Hero.isJump:
                self.Hero.isJump = True
            else:
                if self.Hero.y - self.Hero.jumpcount + self.Hero.height < 512:
                    if self.Hero.jumpcount > 0:
                        if self.Hero.y - self.Hero.jumpcount < self.move_details:
                            self.Change_count = (self.move_details - (self.Hero.y - self.Hero.jumpcount - 1))
                            self.count += self.Change_count

                            for i in range(self.r):
                                self.Blocks_list[i].y += self.Change_count

                                if self.Blocks_list[i].y > 512:
                                    del self.Blocks_list[i]
                                    self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50,
                                                                                                                  200)

                                    if self.count // 1000 % 30 == 0 and self.count > 10000:
                                        self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
                                    elif random.randrange(30 - self.count // 1000 % 29) == 0:
                                        self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
                                    else:
                                        self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))

                            self.Hero.y = self.move_details
                        else:
                            self.Hero.y -= self.Hero.jumpcount

                    if self.Hero.jumpcount < 0:
                        self.Hero.y -= self.Hero.jumpcount
                    self.Hero.jumpcount -= 1
                else:
                    self.isRunning = False
            for i in range(self.r):
                if (self.Hero.x + self.Hero.width >= self.Blocks_list[i].x and
                    self.Hero.x <= self.Blocks_list[i].x_w) and \
                        self.Hero.y - self.Hero.jumpcount + self.Hero.height >= self.Blocks_list[i].y > self.Hero.y + self.Hero.height:
                    self.Hero.jumpcount = self.Hero.JumpHeight
                    self.Hero.isJump = False
                    if self.Blocks_list[i].Check_del:
                        del self.Blocks_list[i]
                        self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50, 200)
                        if self.count // 1000 % 30 == 0 and self.count > 10000:
                            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
                        elif random.randrange(30 - self.count // 1000 % 29) == 0:
                            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
                        else:
                            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))
                    else:
                        self.Hero.y = self.Blocks_list[i].y - self.Hero.height
            if keys[pygame.K_UP]:
                self.play_music(self.music)
            self.draw_win()

        self.isRunning = True
        self.music = 0
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.game_over()
        pygame.quit()
