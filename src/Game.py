import pygame
import random
from Block import Block
from Hero import Hero
from Jetpack import *


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((320, 512 + 64))

        pygame.display.set_caption("Doodle Jump")

        self.background = pygame.image.load("../assets/pictures/background_s.png")
        self.bottom = pygame.image.load("../assets/pictures/Bottom.png")

        self.y_loc = 450  # position of spawning blocks
        self.Blocks_list = []  # list of active blocks
        self.Blocks_list.append(Block(150, 501, False, self))
        for i in range(10):
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))
            self.y_loc -= random.randrange(50, 150)
        self.clock = pygame.time.Clock()  # fps
        self.score = 0  # player's score
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)  # font
        self.textsurface = self.myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))  # first message
        self.music = 1  # number of playing music
        self.isRunning = True  # if main cycle is going
        self.change_y_position = 0  # coordinates changing of objects' position
        self.Hero = Hero(self)
        self.key = 0  # number of music
        self.jetpack_flag = False
        self.jetpack_begin = None
        self.is_jet_on_block = False
        self.Jetpack = None

    def create_block(self):
        self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50, 200)
        if self.score // 1000 % 30 == 0 and self.score > 10000:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        elif random.randrange(30 - self.score // 1000 % 29) == 0:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        else:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))

    def touch_block(self):
        for block in self.Blocks_list:
            if (self.Hero.right_side >= block.x and self.Hero.x <= block.right_side) and self.Hero.next_legs_position\
                    >= block.y > self.Hero.legs_position:
                self.Hero.push_off(block)
                if block.check_del:
                    self.Blocks_list.remove(block)
                    self.create_block()

    def game_over(self):
        if self.music == 0:
            self.play_music(0)
        pygame.display.update()
        self.win.blit(self.background, (0, 0))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.win.blit(self.textsurface, (120, 100))
        self.textsurface = self.myfont.render('ХА-ХА-ХА'.format(int(self.score)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (120, 200))
        self.textsurface = self.myfont.render('ВЫ СЛИШКОМ ПЛОХО ИГРАЛИ!\n СЧЕТ:{}'.format(int(self.score)), False,
                                              (0, 0, 0))
        self.win.blit(self.textsurface, (0, 300))
        self.textsurface = self.myfont.render('СЧЕТ:{}'.format(int(self.score)), False, (0, 0, 0))
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
        self.textsurface = self.myfont.render('Score: {}'.format(int(self.score)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (0, 0))
        for block in self.Blocks_list:
            block.draw()
        self.Hero.draw()
        self.Hero.draw_slot()
        if self.is_jet_on_block:
            self.Jetpack.catch_jetpack()
        pygame.display.update()

    def run(self):
        while self.isRunning:
            if 40000 >= self.score >= 10000:
                self.clock.tick(30 + self.score // 1000 - 10)
            elif self.score > 40000:
                self.clock.tick(60)
            else:
                self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if 0 < self.score < 50 and not self.is_jet_on_block:
                self.is_jet_on_block = True
                self.Jetpack = Jetpack(self)
            if self.is_jet_on_block and (
                    self.Jetpack.y < self.Hero.y < self.Jetpack.y + 36 or self.Jetpack.y < self.Hero.y + self.Hero.height < self.Jetpack.y + 36) and (
                    self.Hero.x + self.Hero.width > self.Jetpack.x > self.Hero.x or self.Hero.x < self.Jetpack.x + 26 < self.Hero.x + self.Hero.width):
                self.Hero.slot = "Jetpack"
                self.is_jet_on_block = False
                self.jetpack_flag = True
                self.Jetpack.jetpack_begin = self.score
            if self.jetpack_flag:
                self.Hero.is_jump = True
                self.Hero.velocity = self.Hero.jump_height + 5
                self.Jetpack.counting_position()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.play_music(self.music)

            self.Hero.move()
            if not self.Hero.is_jump:
                self.Hero.is_jump = True
            else:
                if self.Hero.next_legs_position < 512:
                    self.change_y_position = self.Hero.objects_falling()
                    self.score += self.change_y_position
                else:
                    self.isRunning = False
                if self.is_jet_on_block:
                    self.Jetpack.y += self.change_y_position
                    if self.Jetpack.y > 512:
                        self.is_jet_on_block = False
                        self.Jetpack = "Deleted"

                for block in self.Blocks_list:
                    block.y += self.change_y_position
                    if block.y > 512:
                        self.Blocks_list.remove(block)
                        self.create_block()
            if self.Jetpack is not None and not self.jetpack_flag and not self.is_jet_on_block:
                self.Jetpack = None
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
