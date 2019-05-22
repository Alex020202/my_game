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
        self.jump_height = 21  # height of jump: 1+2+3+4+..+x
        self.isJump = False  # if character jumping
        self.velocity = self.jump_height  # position of jump
        self.change_count = my_game.change_count
        self.my_game = my_game
        self.right_side = self.x + self.width
        self.next_legs_position = self.y - self.velocity + self.height
        self.legs_position = self.y + self.height
        self.next_y_position = self.y - self.velocity

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
            self.isJump = True
            self.velocity = self.jump_height + 10

    def jump(self):
        if self.next_legs_position < 512:
            if self.next_y_position < self.my_game.move_details:
                self.my_game.change_count = (self.my_game.move_details - (self.next_y_position - 1))
                self.my_game.count += self.my_game.change_count

                for block in self.my_game.Blocks_list:
                    block.y += self.my_game.change_count
                    if block.y > 512:
                        self.my_game.Blocks_list.remove(block)
                        self.my_game.create_block()

                self.y = self.my_game.move_details
            else:
                self.y = self.next_y_position
            self.velocity -= 1
        else:
            self.my_game.isRunning = False

    def push_off(self, block):
        self.y = block.y - self.height
        self.velocity = self.jump_height
        self.isJump = False

    def change_variables(self):
        self.right_side = self.x + self.width
        self.next_legs_position = self.y - self.velocity + self.height
        self.legs_position = self.y + self.height
        self.next_y_position = self.y - self.velocity
