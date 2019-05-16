import pygame
import random


class Block:
    def __init__(self, x, y, Check_del):
        self.x = x
        self.y = y
        self.x_w = x + 30
        self.Check_del = Check_del
        if not self.Check_del:
            self.block_image = pygame.image.load("../assets/pictures/block.png")
        else:
            self.block_image = pygame.image.load("../assets/pictures/white_block.png")

    def draw_block(self, my_game):
        my_game.win.blit(self.block_image, (self.x, self.y))


