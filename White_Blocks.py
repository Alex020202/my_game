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