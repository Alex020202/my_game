import pygame
import random
from Jetpack import *
from Blocks import *
from White_Blocks import *

pygame.init()
win = pygame.display.set_mode((320, 512 + 64))

pygame.display.set_caption("Doodle Jump")

jumpRight = [
    pygame.image.load("assets/pictures/right_up_s.png"),
    pygame.image.load("assets/pictures/right_down_s.png")
]

jumpLeft = [
    pygame.image.load("assets/pictures/left_up_s.png"),
    pygame.image.load("assets/pictures/left_down_s.png")
]

jumpFront = [
    pygame.image.load("assets/pictures/front_up_s.png"),
    pygame.image.load("assets/pictures/front_down_s.png")
]

background = pygame.image.load("assets/pictures/background_s.png")
Bottom = pygame.image.load("assets/pictures/Bottom.png")

block_image = [
    pygame.image.load("assets/pictures/block.png"),
    pygame.image.load("assets/pictures/white_block.png")
]

class Blocks:
    def __init__(self, x, y):
        global width
        self.x = x
        self.y = y
        self.x_w = x + width
        self.Check_del = False
        self.block_image = pygame.image.load("assets/pictures/block.png")

    def drawBlock(self):
        global block_image
        win.blit(self.block_image, (self.x, self.y))

class White_Blocks:
    def __init__(self, x, y):
        global white_block
        self.x = x
        self.y = y
        self.x_w = x + width
        self.Check_del = True
        self.block_image = pygame.image.load("assets/pictures/white_block.png")

    def drawBlock(self):
        global block_image
        win.blit(self.block_image, (self.x, self.y))

class Jetpack:
    def __init__(self, x, y):
        global position
        self.position = position
        self.x = x
        self.y = y + 15
        self.isJet = True
        self.jetpackLeft_1 = []
        self.jetpackLeft_2 = []
        self.jetpackRight_1 = []
        self.jetpackRight_2 = []
        for number in range(10):
            self.jetpackLeft_1.append(pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackLeft_2.append(pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}2.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_1.append(pygame.image.load("assets/pictures/JetpackRight/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_2.append(pygame.image.load("assets/pictures/JetpackRight/jetpack_{}2.png".format(str(number))))
        self.jetpackFallRight = pygame.image.load("assets/pictures/JetpackRight/jetpack_10.png")
        self.jetpackFallLeft = pygame.image.load("assets/pictures/JetpackLeft/jetpack_10.png")
        self.jetpackCatch = pygame.image.load("assets/pictures/Catch_Jetpack.png")

    def drawJetpack(self):
        global animCount, left, right, S, jetpack_flag, x_fall
        if animCount >= 4:
            animCount = 0
        if self.position < 10 and jetpack_flag:
            if left:
                if animCount == 0:
                    win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
            elif right:
                if animCount == 0:
                    win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                else:
                    animCount += 1
            else:
                if animCount == 0:
                    win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
        elif self.position >= 10 and jetpack_flag:
            if left_fall:
                self.y += S
                S += 5
                win.blit(self.jetpackFallLeft, (x_fall, self.y))
            elif right_fall:
                self.y += S
                S += 5
                win.blit(self.jetpackFallRight, (x_fall - width - 9, self.y))
            else:
                self.y += S
                S += 5
                win.blit(self.jetpackFallLeft, (x_fall + width, self.y))
                win.blit(self.jetpackFallRight, (x_fall - 26, self.y))
        if self.y > 512 - 32:
            jetpack_flag = False

    def catchJetpack(self):
        win.blit(self.jetpackCatch, (self.x + width - 8, self.y))

clock = pygame.time.Clock()
catch = False
S = 0
x = 150
y = 400
width = 30
height = 60
speed = 10
Half_win = 512 / 2 - 50

JumpHeight = 21
isJump = False
jumpCount = JumpHeight

left = False
right = False
y_loc = 450
Blocks_list = []
r = 10
count = 0
white_block = False

animCount = 0
jetpackBegin = 0
jetpack_flag = False

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)

Blocks_list.append(Blocks(150, 501))
for i in range(1, r):
    Blocks_list.append(Blocks(random.randrange(320 - 40), y_loc))
    y_loc -= random.randrange(50, 150)


def Game_over():
    play_music(0)
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    pygame.display.update()
    win.blit(background, (0, 0))
    textsurface = myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))
    win.blit(textsurface, (120, 100))
    textsurface = myfont.render('ХА-ХА-ХА'.format(int(count)), False, (0, 0, 0))
    win.blit(textsurface, (120, 200))
    textsurface = myfont.render('ВЫ СЛИШКОМ ПЛОХО ИГРАЛИ!\n СЧЕТ:{}'.format(int(count)), False, (0, 0, 0))
    win.blit(textsurface, (0, 300))
    textsurface = myfont.render('СЧЕТ:{}'.format(int(count)), False, (0, 0, 0))
    win.blit(textsurface, (120, 400))


def play_music(key):
    global music
    if key != 0:
        key = key % 5 + 1
    if key == 0 and music == 0:
        pygame.mixer.music.load("assets/music/strashnye-zvuki-d-yavol-skiy-smeh.mp3")
        pygame.mixer.music.play()
        music += 1
    elif key == 1:
        pygame.mixer.music.load("assets/music/coldplay_feat_beyonce_-_hymn_for_the_weekend_(zf.fm).mp3")
        pygame.mixer.music.play()
        music += 1
    elif key == 2:
        pygame.mixer.music.load("assets/music/Celldweller - Frozen.mp3")
        pygame.mixer.music.play()
        music += 1
    elif key == 3:
        pygame.mixer.music.load("assets/music/teddybears_sthlm_and_mad_cobra_-_cobrastyle_(zaycev.net).mp3")
        pygame.mixer.music.play()
        music += 1
    elif key == 4:
        pygame.mixer.music.load("assets/music/ylvis_-_what_does_the_fox_say_(zaycev.net).mp3")
        pygame.mixer.music.play()
        music += 1
    elif key == 5:
        pygame.mixer.music.load("assets/music/tiesto__sevenn_-_boom_2017_(zf.fm).mp3")
        pygame.mixer.music.play()
        music += 1


def drawWin():
    global right, left, animCount
    win.fill((0, 0, 0))
    win.blit(background, (0, 0))
    win.blit(Bottom, (0, 511))
    textsurface = myfont.render('Score: {}'.format(int(count)), False, (0, 0, 0))
    win.blit(textsurface, (0, 0))

    for i in range(r):
        Blocks_list[i].drawBlock()
    if jetpack_flag:
        for j in range(2):
            if jetpack_flag:
                Jetpack(x, y).drawJetpack()
    if isJet:
        Jet.catchJetpack()
    pygame.display.update()
    if isJump:
        if left:
            win.blit(jumpLeft[0], (x - 16, y))
        elif right:
            win.blit(jumpRight[0], (x, y))
        else:
            win.blit(jumpFront[0], (x, y))
    else:
        if left_fall:
            win.blit(jumpLeft[1], (x - 16, y))
        elif right_fall:
            win.blit(jumpRight[1], (x, y))
        else:
            win.blit(jumpFront[1], (x, y))
    pygame.display.update()


left_fall = False
right_fall = False
music = 1
play_music(1)
flag = False
run = True
isJet = False
position = -1
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if 50 > count % 20000 > 0 and not isJet and count > 20000:
        Jet = Jetpack(Blocks_list[8 - 1].x - 13, Blocks_list[8 - 1].y - 47)
        isJet = True
    if isJet and (Jet.y < y < Jet.y + 36 or Jet.y < y + height < Jet.y + 36) and (Jet.x < x < Jet.x + 26 or Jet.x < x + width < Jet.x + 26):
        jetpack_flag = True
        jetpackBegin = count
        del Jet
        isJet = False

    if jetpack_flag:
        if 0 <= count - jetpackBegin < 200:
            position = 0
        elif 200 <= count - jetpackBegin < 400:
            position = 1
        elif 400 < count - jetpackBegin < 600:
            position = 2
        elif 600 < count - jetpackBegin < 800:
            position = 3
        elif 800 < count - jetpackBegin < 1000:
            position = 4
        elif 1000 < count - jetpackBegin < 1200:
            position = 5
        elif 1200 < count - jetpackBegin < 1400:
            position = 6
        elif 1400 < count - jetpackBegin < 1600:
            position = 7
        elif 1600 < count - jetpackBegin < 1800:
            position = 8
        elif 1800 < count - jetpackBegin < 2000:
            position = 9
        elif 2000 < count - jetpackBegin:
            position += 1
            if position == 10:
                x_fall = x
                if right:
                    right_fall = True
                elif left:
                    left_fall = True
                else:
                    right_fall = False
                    left_fall = False
        isJump = True
        jumpCount = JumpHeight

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if x - speed + width > 0:
            x -= speed
            left = True
            right = False
        else:
            x = 320
    elif keys[pygame.K_RIGHT]:
        if x + speed < 320:
            x += speed
            left = False
            right = True
        else:
            x = 0
    else:
        left = False
        right = False
    if keys[pygame.K_SPACE]:
        isJump = True
        jumpCount = JumpHeight
    if not isJump:
        isJump = True
    else:
        if y - jumpCount + height < 512:
            if jumpCount > 0:
                if y - jumpCount < Half_win:
                    Change_count = (Half_win - (y - jumpCount))
                    count += Change_count
                    if isJet:
                        Jet.y += Change_count
                    for i in range(r):
                        Blocks_list[i].y += Change_count

                        if Blocks_list[i].y > 512:
                            del Blocks_list[i]
                            y_loc = Blocks_list[len(Blocks_list) - 1].y - random.randrange(50, 200)

                            if count // 1000 % 30 == 0 and count > 10000:
                                Blocks_list.append(White_Blocks(random.randrange(320 - 40), y_loc))
                            elif random.randrange(30 - count // 1000 % 29) == 0:
                                Blocks_list.append(White_Blocks(random.randrange(320 - 40), y_loc))
                            else:
                                Blocks_list.append(Blocks(random.randrange(320 - 40), y_loc))
                        if isJet:
                            if Jet.y > 512:
                                del Jet
                                isJet = False
                    y = Half_win
                else:
                    y -= jumpCount

            if jumpCount < 0:
                y -= jumpCount
            jumpCount -= 1
        else:
            run = False
    for i in range(r):
        if (x + width >= Blocks_list[i].x and x <= Blocks_list[i].x_w) and y - jumpCount + height >= Blocks_list[i].y > y + height:
            jumpCount = JumpHeight
            isJump = False
            if Blocks_list[i].Check_del:
                del Blocks_list[i]
                y_loc = Blocks_list[len(Blocks_list) - 1].y - random.randrange(50, 200)
                if count // 1000 % 30 == 0 and count > 10000:
                    Blocks_list.append(White_Blocks(random.randrange(320 - 40), y_loc))
                elif random.randrange(30 - count // 1000 % 29) == 0:
                    Blocks_list.append(White_Blocks(random.randrange(320 - 40), y_loc))
                else:
                    Blocks_list.append(Blocks(random.randrange(320 - 40), y_loc))
            else:
                y = Blocks_list[i].y - height
    if keys[pygame.K_UP]:
        play_music(music)
    drawWin()

run = True
music = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    Game_over()
pygame.quit()
