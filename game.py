import pygame
import random
from Jetpack import *
from White_Blocks import *
from Blocks import *


pygame.init()


class Blocks:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_w = x + 30
        self.Check_del = False
        self.block_image = pygame.image.load("assets/pictures/block.png")

    def draw_block(self):
        Game.win.blit(self.block_image, (self.x, self.y))


class WhiteBlocks:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_w = x + 30
        self.Check_del = True
        self.block_image = pygame.image.load("assets/pictures/white_block.png")

    def draw_block(self):
        Game.win.blit(self.block_image, (self.x, self.y))

class Jetpack:
    def __init__(self, x, y):
        self.position = Game.position
        self.x = Game.x
        self.y = Game.y + 15
        self.isJet = True
        self.jetpackLeft_1 = []
        self.jetpackLeft_2 = []
        self.jetpackRight_1 = []
        self.jetpackRight_2 = []
        for number in range(10):
            self.jetpackLeft_1.append(
                pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackLeft_2.append(
                pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}2.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_1.append(
                pygame.image.load("assets/pictures/JetpackRight/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_2.append(
                pygame.image.load("assets/pictures/JetpackRight/jetpack_{}2.png".format(str(number))))
        self.jetpackFallRight = pygame.image.load("assets/pictures/JetpackRight/jetpack_10.png")
        self.jetpackFallLeft = pygame.image.load("assets/pictures/JetpackLeft/jetpack_10.png")
        self.jetpackCatch = pygame.image.load("assets/pictures/Catch_Jetpack.png")

    def draw_jetpack(self):
        global animCount, left, right, S, jetpack_flag, x_fall
        if animCount >= 4:
            animCount = 0
        if self.position < 10 and jetpack_flag:
            if left:
                if animCount == 0:
                    Game.win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    Game.win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
            elif right:
                if animCount == 0:
                    Game.win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                elif animCount == 2:
                    Game.win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                else:
                    animCount += 1
            else:
                if animCount == 0:
                    Game.win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    Game.win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    Game.win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    Game.win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
        elif self.position >= 10 and jetpack_flag:
            if left_fall:
                self.y += S
                S += 5
                Game.win.blit(self.jetpackFallLeft, (x_fall, self.y))
            elif right_fall:
                self.y += S
                S += 5
                Game.win.blit(self.jetpackFallRight, (x_fall - width - 9, self.y))
            else:
                self.y += S
                S += 5
                Game.win.blit(self.jetpackFallLeft, (x_fall + width, self.y))
                Game.win.blit(self.jetpackFallRight, (x_fall - 26, self.y))
        if self.y > 512 - 32:
            jetpack_flag = False

    def catch_jetpack(self):
        Game.win.blit(self.jetpackCatch, (self.x + width - 8, self.y))


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((320, 512 + 64))

        pygame.display.set_caption("Doodle Jump")

        self.jumpRight = [
            pygame.image.load("assets/pictures/right_up_s.png"),
            pygame.image.load("assets/pictures/right_down_s.png")
        ]

        self.jumpLeft = [
            pygame.image.load("assets/pictures/left_up_s.png"),
            pygame.image.load("assets/pictures/left_down_s.png")
        ]

        self.jumpFront = [
            pygame.image.load("assets/pictures/front_up_s.png"),
            pygame.image.load("assets/pictures/front_down_s.png")
        ]

        self.background = pygame.image.load("assets/pictures/background_s.png")
        self.bottom = pygame.image.load("assets/pictures/Bottom.png")

        self.block_image = [
            pygame.image.load("assets/pictures/block.png"),
            pygame.image.load("assets/pictures/white_block.png")
        ]
        self.y_loc = 450  # position of spawning blocks
        self.r = 10  # Number of spawning blocks
        self.Blocks_list = []
        self.Blocks_list.append(Blocks(150, 501))

        self.clock = pygame.time.Clock()
        self.catch = False  # if non-catched jetpack is
        self.S = 0  # speed of falling jetpack
        self.x = 150  # x position of character
        self.y = 400  # y position of character
        self.width = 30  # width of character
        self.height = 60  # height of character
        self.speed = 10  # left-right moving speed
        self.move_details = 512 / 2 - 50  # line which character can't outstep

        self.JumpHeight = 21  # height of jump: 1+2+3+4+..+x
        self.isJump = False  # if character jumping
        self.jumpCount = self.JumpHeight  # position of jump

        self.left = False  # if character moves left
        self.right = False  # if character moves right

        self.count = 0  # player's score
        self.white_block = False  # if white block is

        self.animCount = 0  # position of jetpack animation at the stage
        self.jetpackBegin = 0  # score of started jetpack
        self.jetpack_flag = False  # if jetpack is

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
        self.textsurface = self.myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))

        self.left_fall = False  # if jetpack fall at left side
        self.right_fall = False  # if jetpack fall at right side
        self.music = 1  # number of playing music
        self.flag = False
        self.run = True  # if main cicle is going
        self.isJet = False  # if object of "jetpack" class is
        self.position = -1  # stage of jetpack animation
        for i in range(1, self.r):
            self.Blocks_list.append(Blocks(random.randrange(320 - 40), self.y_loc))
            self.y_loc -= random.randrange(50, 150)

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
            pygame.mixer.music.load("assets/music/strashnye-zvuki-d-yavol-skiy-smeh.mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 1:
            pygame.mixer.music.load("assets/music/coldplay_feat_beyonce_-_hymn_for_the_weekend_(zf.fm).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 2:
            pygame.mixer.music.load("assets/music/Celldweller - Frozen.mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 3:
            pygame.mixer.music.load("assets/music/teddybears_sthlm_and_mad_cobra_-_cobrastyle_(zaycev.net).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 4:
            pygame.mixer.music.load("assets/music/ylvis_-_what_does_the_fox_say_(zaycev.net).mp3")
            pygame.mixer.music.play()
            self.music += 1
        elif self.key == 5:
            pygame.mixer.music.load("assets/music/tiesto__sevenn_-_boom_2017_(zf.fm).mp3")
            pygame.mixer.music.play()
            self.music += 1

    def draw_win(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.background, (0, 0))
        self.win.blit(self.bottom, (0, 511))
        self.textsurface = self.myfont.render('Score: {}'.format(int(self.count)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (0, 0))

        for i in range(self.r):
            self.Blocks_list[i].draw_block()
        if self.jetpack_flag:
            for j in range(2):
                if jetpack_flag:
                    Jetpack(x, y).draw_jetpack()
        if self.isJet:
            jet.catch_jetpack()
        pygame.display.update()
        if self.isJump:
            if self.left:
                self.win.blit(self.jumpLeft[0], (self.x - 16, self.y))
            elif self.right:
                self.win.blit(self.jumpRight[0], (self.x, self.y))
            else:
                self.win.blit(self.jumpFront[0], (self.x, self.y))
        else:
            if self.left_fall:
                self.win.blit(self.jumpLeft[1], (self.x - 16, self.y))
            elif self.right_fall:
                self.win.blit(self.jumpRight[1], (self.x, self.y))
            else:
                self.win.blit(self.jumpFront[1], (self.x, self.y))
        pygame.display.update()

    def run_game(self):
        while self.run:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            if 50 > self.count % 20000 > 0 and not self.isJet:
                jet = Jetpack(self.Blocks_list[8 - 1].x - 13, self.Blocks_list[8 - 1].y - 47)
                self.isJet = True
            if self.isJet and (jet.y < self.y < jet.y + 36 or jet.y < self.y + self.height < jet.y + 36) and (
                    jet.x < self.x < jet.x + 26 or jet.x < self.x + self.width < jet.x + 26):
                self.jetpack_flag = True
                self.jetpackBegin = self.count
                del jet
                self.isJet = False

            if self.jetpack_flag:
                if 0 <= self.count - self.jetpackBegin < 200:
                    self.position = 0
                elif 200 <= self.count - self.jetpackBegin < 400:
                    self.position = 1
                elif 400 < self.count - self.jetpackBegin < 600:
                    self.position = 2
                elif 600 < self.count - self.jetpackBegin < 800:
                    self.position = 3
                elif 800 < self.count - self.jetpackBegin < 1000:
                    self.position = 4
                elif 1000 < self.count - self.jetpackBegin < 1200:
                    self.position = 5
                elif 1200 < self.count - self.jetpackBegin < 1400:
                    self.position = 6
                elif 1400 < self.count - self.jetpackBegin < 1600:
                    self.position = 7
                elif 1600 < self.count - self.jetpackBegin < 1800:
                    self.position = 8
                elif 1800 < self.count - self.jetpackBegin < 2000:
                    self.position = 9
                elif 2000 < self.count - self.jetpackBegin:
                    self.position += 1
                    if self.position == 10:
                        self.x_fall = x
                        if self.right:
                            self.right_fall = True
                        elif self.left:
                            self.left_fall = True
                        else:
                            self.right_fall = False
                            self.left_fall = False
                self.isJump = True
                self.jumpCount = self.JumpHeight - 10

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.x - self.speed + self.width > 0:
                    self.x -= self.speed
                    self.left = True
                    self.right = False
                else:
                    x = 320
            elif keys[pygame.K_RIGHT]:
                if self.x + self.speed < 320:
                    self.x += self.speed
                    self.left = False
                    self.right = True
                else:
                    x = 0
            else:
                self.left = False
                self.right = False
            if keys[pygame.K_SPACE]:
                self.isJump = True
                self.jumpCount = self.JumpHeight + 10
            if not self.isJump:
                self.isJump = True
            else:
                if self.y - self.jumpCount + self.height < 512:
                    if self.jumpCount > 0:
                        if self.y - self.jumpCount < self.move_details:
                            self.Change_count = (self.move_details - (self.y - self.jumpCount))
                            self.count += self.Change_count
                            if self.isJet:
                                jet.y += self.Change_count
                            for i in range(self.r):
                                self.Blocks_list[i].y += self.Change_count

                                if self.Blocks_list[i].y > 512:
                                    del self.Blocks_list[i]
                                    self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50,
                                                                                                                  200)

                                    if self.count // 1000 % 30 == 0 and self.count > 10000:
                                        self.Blocks_list.append(WhiteBlocks(random.randrange(320 - 40), self.y_loc))
                                    elif random.randrange(30 - self.count // 1000 % 29) == 0:
                                        self.Blocks_list.append(WhiteBlocks(random.randrange(320 - 40), self.y_loc))
                                    else:
                                        self.Blocks_list.append(Blocks(random.randrange(320 - 40), self.y_loc))
                                if self.isJet:
                                    if jet.y > 512:
                                        del jet
                                        self.isJet = False
                            self.y = self.move_details
                        else:
                            self.y -= self.jumpCount

                    if self.jumpCount < 0:
                        self.y -= self.jumpCount
                    self.jumpCount -= 1
                else:
                    self.run = False
            for i in range(self.r):
                if (self.x + self.width >= self.Blocks_list[i].x and
                    self.x <= self.Blocks_list[i].x_w) and \
                        self.y - self.jumpCount + self.height >= self.Blocks_list[i].y > self.y + self.height:
                    self.jumpCount = self.JumpHeight
                    self.isJump = False
                    if self.Blocks_list[i].Check_del:
                        del self.Blocks_list[i]
                        self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50, 200)
                        if self.count // 1000 % 30 == 0 and self.count > 10000:
                            self.Blocks_list.append(WhiteBlocks(random.randrange(320 - 40), self.y_loc))
                        elif random.randrange(30 - self.count // 1000 % 29) == 0:
                            self.Blocks_list.append(WhiteBlocks(random.randrange(320 - 40), self.y_loc))
                        else:
                            self.Blocks_list.append(Blocks(random.randrange(320 - 40), self.y_loc))
                    else:
                        self.y = self.Blocks_list[i].y - self.height
            if keys[pygame.K_UP]:
                self.play_music(self.music)
            self.draw_win()

        self.run = True
        self.music = 0
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.game_over()
        pygame.quit()


if __name__ == '__main__':
    Game = Game()
    Game.run_game()


