import pygame
from Jetpack import Jetpack


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
        self.jump_height = 20  # height of jump: 1+2+3+4+..+x
        self.is_jump = False  # if character jumping
        self.velocity = self.jump_height  # position of jump
        self.my_game = my_game
        self.right_side = self.x + self.width  # right side of hero
        self.next_legs_position = self.y - self.velocity + self.height
        self.legs_position = self.y + self.height
        self.next_y_position = self.y - self.velocity
        self.move_details = 512 / 2 - 50  # line which character can't outstep
        self.slot = "Empty"

    def draw(self):
        if self.is_jump:
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

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x - self.speed + self.width > 0:
                self.x -= self.speed
                self.left = True
                self.right = False
            else:
                self.x = 320
        elif keys[pygame.K_RIGHT]:
            if self.x + self.speed < 320:
                self.x += self.speed
                self.left = False
                self.right = True
            else:
                self.x = 0
        else:
            self.left = False
            self.right = False
        if keys[pygame.K_SPACE]:
            self.is_jump = True
            self.velocity = self.jump_height

    def objects_falling(self):
        change = 0
        if self.next_y_position < self.move_details:
            change = self.move_details - self.next_y_position + 1
            self.y = self.move_details
        else:
            self.y = self.next_y_position
        self.velocity -= 1
        return change

    def push_off(self, block):
        self.y = block.y - self.height
        self.velocity = self.jump_height
        self.is_jump = False

    def change_variables(self):
        self.right_side = self.x + self.width
        self.next_legs_position = self.y - self.velocity + self.height
        self.legs_position = self.y + self.height
        self.next_y_position = self.y - self.velocity

    def draw_slot(self):
        if self.slot == "Jetpack":
            self.my_game.Jetpack.draw()
