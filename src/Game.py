import pygame
import random
from Block import *
from Hero import *


class Game:
    def __init__(self):
        self.isJet = False  # if object of "jetpack" class is
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
        self.count = 0  # player's score
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.textsurface = self.myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))
        self.music = 1  # number of playing music
        self.isRunning = True  # if main cycle is going
        self.change_count = 0  # coordinates changing of objects' position
        self.Hero = Hero(self)

    def create_block(self):
        self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50,
                                                                                      200)
        if self.count // 1000 % 30 == 0 and self.count > 10000:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        elif random.randrange(30 - self.count // 1000 % 29) == 0:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        else:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))

    def touch_block(self):
        for block in self.Blocks_list:
            if (self.Hero.right_side >= block.x and self.Hero.x <= block.x_w) and self.Hero.next_legs_position >= block.y > self.Hero.legs_position:
                self.Hero.push_off(block)
                if block.сheck_del:
                    self.Blocks_list.remove(block)
                    self.create_block()

    def game_over(self):
        if self.music == 0:
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
        if key != 0:
            self.key = key % 5 + 1
        else:
            self.key = 0

        if self.key == 0 and self.music == 0:
            pygame.mixer.music.load("../assets/music/strashnye-zvuki-d-yavol-skiy-smeh.mp3")
        elif self.key == 1:
            pygame.mixer.music.load("../assets/music/coldplay_feat_beyonce_-_hymn_for_the_weekend_(zf.fm).mp3")
        elif self.key == 2:
            pygame.mixer.music.load("../assets/music/Celldweller - Frozen.mp3")
        elif self.key == 3:
            pygame.mixer.music.load("../assets/music/teddybears_sthlm_and_mad_cobra_-_cobrastyle_(zaycev.net).mp3")
        elif self.key == 4:
            pygame.mixer.music.load("../assets/music/ylvis_-_what_does_the_fox_say_(zaycev.net).mp3")
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
        for block in self.Blocks_list:
            block.draw()
        self.Hero.draw()
        pygame.display.update()

    def run(self):
        while self.isRunning:

            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.play_music(self.music)

            self.Hero.move()
            if not self.Hero.isJump:
                self.Hero.isJump = True
            else:
                self.Hero.jump()
            self.Hero.change_variables()
            self.touch_block()
            self.draw_win()

        self.isRunning = True
        self.music = 0
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
            self.game_over()

        pygame.quit()
