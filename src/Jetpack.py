import pygame
import random


class Jetpack:
    def __init__(self, my_game):
        self.left = False
        self.right = False
        self.win = my_game.win
        self.my_game = my_game
        self.Hero = my_game.Hero
        self.jetpack_flag = my_game.jetpack_flag
        self.position = 0

        if my_game.is_jet_on_block:
            self.x = my_game.Blocks_list[6].x + 8
            self.y = my_game.Blocks_list[6].y - 36
        else:
            self.x = my_game.Hero.x
            self.y = my_game.Hero.y + 15
        self.jetpackLeft_1 = []
        self.jetpackLeft_2 = []
        self.jetpackRight_1 = []
        self.jetpackRight_2 = []
        self.jetpack_begin = self.my_game.score
        self.right_fall = False
        self.y_fall = None
        self.x_fall = None
        self.left_fall = False
        self.animcount = 0
        self.jetpack_animation_velocity = self.my_game.FPS / 30 * 2

        for number in range(10):
            self.jetpackLeft_1.append(
                pygame.image.load("../assets/pictures/JetpackLeft/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackLeft_2.append(
                pygame.image.load("../assets/pictures/JetpackLeft/jetpack_{}2.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_1.append(
                pygame.image.load("../assets/pictures/JetpackRight/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_2.append(
                pygame.image.load("../assets/pictures/JetpackRight/jetpack_{}2.png".format(str(number))))
        self.jetpackFallRight = pygame.image.load("../assets/pictures/JetpackRight/jetpack_10.png")
        self.jetpackFallLeft = pygame.image.load("../assets/pictures/JetpackLeft/jetpack_10.png")
        self.jetpackCatch = pygame.image.load("../assets/pictures/Catch_Jetpack.png")

    def counting_position(self):
        if 0 <= (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 200:
            self.position = 0
            self.Hero.velocity = self.Hero.jump_height - 5
        elif 200 <= (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 400:
            self.position = 1
            self.Hero.velocity = self.Hero.jump_height - 3
        elif 400 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 600:
            self.position = 2
            self.Hero.velocity = self.Hero.jump_height - 1
        elif 600 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 800:
            self.position = 3
            self.Hero.velocity = self.Hero.jump_height + 1
        elif 800 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 1000:
            self.position = 4
            self.Hero.velocity = self.Hero.jump_height + 3
        elif 1000 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 1200:
            self.position = 5
            self.Hero.velocity = self.Hero.jump_height + 5
        elif 1200 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 1400:
            self.position = 6
            self.Hero.velocity = self.Hero.jump_height + 3
        elif 1400 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 1600:
            self.position = 7
            self.Hero.velocity = self.Hero.jump_height + 1
        elif 1600 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 1800:
            self.position = 8
            self.Hero.velocity = self.Hero.jump_height - 1
        elif 1800 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity < 2000:
            self.position = 9
            self.Hero.velocity = self.Hero.jump_height - 3
        elif 2000 < (self.my_game.score - self.jetpack_begin) / self.jetpack_animation_velocity :
            self.position += 1
            self.Hero.velocity = self.Hero.jump_height - 5
            if self.position == 10:
                self.x_fall = self.Hero.x
                self.y_fall = self.Hero.y
                if self.Hero.right:
                    self.right_fall = True
                elif self.Hero.left:
                    self.left_fall = True
                else:
                    self.right_fall = False
                    self.left_fall = False

    def draw(self):
        if self.animcount >= 2:
            self.animcount = 0
        if self.position < 10:
            if self.Hero.left:
                if self.animcount == 0:
                    self.win.blit(self.jetpackLeft_1[self.position], (self.Hero.x + self.Hero.width - 8, self.Hero.y + 15))
                    self.animcount += 1
                elif self.animcount == 1:
                    self.win.blit(self.jetpackLeft_2[self.position], (self.Hero.x + self.Hero.width - 8, self.Hero.y + 15))
                    self.animcount += 1
                else:
                    self.animcount += 1
            elif self.Hero.right:
                if self.animcount == 0:
                    self.win.blit(self.jetpackRight_1[self.position], (self.Hero.x - 8 - 9, self.Hero.y + 15))
                    self.animcount += 1
                elif self.animcount == 1:
                    self.win.blit(self.jetpackRight_2[self.position], (self.Hero.x - 8 - 9, self.Hero.y + 15))
                    self.animcount += 1
                else:
                    self.animcount += 1
            else:
                if self.animcount == 0:
                    self.win.blit(self.jetpackRight_1[self.position], (self.Hero.x - 8 - 9, self.Hero.y + 15))
                    self.win.blit(self.jetpackLeft_1[self.position], (self.Hero.x + self.Hero.width - 8, self.Hero.y + 15))
                    self.animcount += 1
                elif self.animcount == 1:
                    self.win.blit(self.jetpackRight_2[self.position], (self.Hero.x - 8 - 9, self.Hero.y + 15))
                    self.win.blit(self.jetpackLeft_2[self.position], (self.Hero.x + self.Hero.width - 8, self.Hero.y + 15))
                    self.animcount += 1
                else:
                    self.animcount += 1
        elif self.position >= 10:
            if self.left_fall:

                self.win.blit(self.jetpackFallLeft, (self.x_fall + 2 * self.position, self.y_fall + self.position ** 2 / 3))
            elif self.right_fall:

                self.win.blit(self.jetpackFallRight, (self.x_fall - self.Hero.width - 9 - 2 * self.position, self.y_fall + self.position ** 2 / 3))
            else:

                self.win.blit(self.jetpackFallLeft, (self.x_fall + self.Hero.width + 2 * self.position, self.y_fall + self.position ** 2 / 3))
                self.win.blit(self.jetpackFallRight, (self.x_fall - 26 - 2 * self.position, self.y_fall + self.position ** 2 / 3))
        if self.y_fall is not None and self.y_fall + self.position ** 2 / 3 > 512 - 60:
            self.my_game.jetpack_flag = False
            self.Hero.slot = None

    def catch_jetpack(self):
        self.win.blit(self.jetpackCatch, (self.x, self.y))
