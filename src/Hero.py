import pygame


class Hero:
    def __init__(self, my_game):
        self.jumpRight = [
            pygame.image.load("../assets/pictures/right_up_s.png"),
            pygame.image.load("../assets/pictures/right_down_s.png")
        ]

        self.jumpLeft = [
            pygame.image.load("../assets/pictures/left_up_s.png"),
            pygame.image.load("../assets/pictures/left_down_s.png")
        ]

        self.jumpFront = [
            pygame.image.load("../assets/pictures/front_up_s.png"),
            pygame.image.load("../assets/pictures/front_down_s.png")
        ]

        self.x = 150  # x position of character
        self.y = 450  # y position of character
        self.width = 30  # width of character
        self.height = 60  # height of character
        self.speed = 10  # left-right moving speed
        self.left = False  # if character moves left
        self.right = False  # if character moves right
        self.win = my_game.win
        self.JumpHeight = 21  # height of jump: 1+2+3+4+..+x
        self.isJump = False  # if character jumping
        self.jumpcount = self.JumpHeight  # position of jump

    def draw(self):
        if self.isJump:
            if self.left:
                self.win.blit(self.jumpLeft[0], (self.x - 16, self.y))
            elif self.right:
                self.win.blit(self.jumpRight[0], (self.x, self.y))
            else:
                self.win.blit(self.jumpFront[0], (self.x, self.y))
        else:
            if self.left:
                self.win.blit(self.jumpLeft[1], (self.x - 16, self.y))
            elif self.right:
                self.win.blit(self.jumpRight[1], (self.x, self.y))
            else:
                self.win.blit(self.jumpFront[1], (self.x, self.y))