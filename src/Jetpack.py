import pygame
import random

class Jetpack:
    def __init__(self, x, y, my_game):
        self.left = my_game.left
        self.right = my_game.right

        self.jetpack_flag = my_game.jetpack_flag
        self.x_fall = my_game.x_fall
        self.position = my_game.position
        if self.jetpack_flag:
            self.x = my_game.x
            self.y = my_game.y + 15
        else:
            self.x = my_game.Blocks_list[9].x + 8
            self.y = my_game.Blocks_list[9].y - 36
            self.isJet = True
        self.S = 0
        self.jetpackLeft_1 = []
        self.jetpackLeft_2 = []
        self.jetpackRight_1 = []
        self.jetpackRight_2 = []
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

    def draw_jetpack(self, my_game):
        if my_game.animcount >= 3:
            my_game.animcount = 0
        if self.position < 10 and self.jetpack_flag:
            if self.left:
                if my_game.animcount == 0:
                    my_game.win.blit(self.jetpackLeft_1[self.position], (self.x + my_game.width - 8, self.y))
                    my_game.animcount += 1
                elif my_game.animcount == 1:
                    my_game.win.blit(self.jetpackLeft_2[self.position], (self.x + my_game.width - 8, self.y))
                    my_game.animcount += 1
                else:
                    my_game.animcount += 1
            elif self.right:
                if my_game.animcount == 0:
                    my_game.win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    my_game.animcount += 1
                elif my_game.animcount == 1:
                    my_game.win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    my_game.animcount += 1
                else:
                    my_game.animcount += 1
            else:
                if my_game.animcount == 0:
                    my_game.win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    my_game.win.blit(self.jetpackLeft_1[self.position], (self.x + my_game.width - 8, self.y))
                    my_game.animcount += 1
                elif my_game.animcount == 1:
                    my_game.win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    my_game.win.blit(self.jetpackLeft_2[self.position], (self.x + my_game.width - 8, self.y))
                    my_game.animcount += 1
                else:
                    my_game.animcount += 1
        elif self.position >= 10 and self.jetpack_flag:
            if my_game.left_fall:

                my_game.win.blit(self.jetpackFallLeft, (self.x_fall + 2 * self.position, self.y + self.position ** 2 / 3))
            elif my_game.right_fall:

                my_game.win.blit(self.jetpackFallRight, (self.x_fall - my_game.width - 9 - 2 * self.position, self.y + self.position ** 2 / 3))
            else:

                my_game.win.blit(self.jetpackFallLeft, (self.x_fall + my_game.width + 2 * self.position, self.y + self.position ** 2 / 3))
                my_game.win.blit(self.jetpackFallRight, (self.x_fall - 26 - 2 * self.position, self.y + self.position ** 2 / 3))
        if self.y + self.position ** 2 / 3 > 512 - 32:
            my_game.jetpack_flag = False

    def catch_jetpack(self, my_game):
        my_game.win.blit(self.jetpackCatch, (self.x , self.y))
