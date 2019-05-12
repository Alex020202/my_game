class Blocks:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_w = x + width
        self.Check_del = False
        self.block_image = pygame.image.load("assets/pictures/block.png")

    def drawBlock(self):
        global block_image
        win.blit(self.block_image, (self.x, self.y))