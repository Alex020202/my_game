import pygame


class Block:
    def __init__(self, x, y, Check_del, my_game):
        self.x = x
        self.y = y
        self.x_w = x + 30
        self.Check_del = Check_del
        self.win = my_game.win
        self.my_game = my_game
        self.Hero = None
        if not self.Check_del:
            self.block_image = pygame.image.load("../assets/pictures/block.png")
        else:
            self.block_image = pygame.image.load("../assets/pictures/white_block.png")

    def draw(self):
        self.win.blit(self.block_image, (self.x, self.y))





