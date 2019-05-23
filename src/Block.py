import pygame


class Block:
    def __init__(self, x, y, сheck_del, my_game):
        self.x = x
        self.y = y
        self.right_side = x + 30
        self.сheck_del = сheck_del  # if block must be removed
        self.win = my_game.win
        self.my_game = my_game
        if not self.сheck_del:
            self.block_image = pygame.image.load("../assets/pictures/block.png")
        else:
            self.block_image = pygame.image.load("../assets/pictures/white_block.png")

    def draw(self):
        self.win.blit(self.block_image, (self.x, self.y))





