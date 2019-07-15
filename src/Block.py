import pygame


class Block:
    def __init__(self, x, y, check_del, my_game):
        self.x = x
        self.y = y
        self.right_side = x + 30
        self.check_del = check_del  # if block must be removed
        self.win = my_game.win
        self.my_game = my_game
        if not self.check_del:
            self.block_image = pygame.image.load("../assets/pictures/block.png")
        else:
            self.block_image = pygame.image.load("../assets/pictures/white_block.png")

    def draw(self):
        self.win.blit(self.block_image, (self.x, self.y))
