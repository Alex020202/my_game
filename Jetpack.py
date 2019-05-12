class Jetpack:
    def __init__(self, x, y):
        global position
        self.position = position
        self.x = x
        self.y = y + 15
        self.isJet = True
        self.jetpackLeft_1 = []
        self.jetpackLeft_2 = []
        self.jetpackRight_1 = []
        self.jetpackRight_2 = []
        for number in range(10):
            self.jetpackLeft_1.append(pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackLeft_2.append(pygame.image.load("assets/pictures/JetpackLeft/jetpack_{}2.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_1.append(pygame.image.load("assets/pictures/JetpackRight/jetpack_{}1.png".format(str(number))))
        for number in range(10):
            self.jetpackRight_2.append(pygame.image.load("assets/pictures/JetpackRight/jetpack_{}2.png".format(str(number))))
        self.jetpackFallRight = pygame.image.load("assets/pictures/JetpackRight/jetpack_10.png")
        self.jetpackFallLeft = pygame.image.load("assets/pictures/JetpackLeft/jetpack_10.png")
        self.jetpackCatch = pygame.image.load("assets/pictures/Catch_Jetpack.png")

    def drawJetpack(self):
        global animCount, left, right, S, jetpack_flag, x_fall
        if animCount >= 4:
            animCount = 0
        if self.position < 10 and jetpack_flag:
            if left:
                if animCount == 0:
                    win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
            elif right:
                if animCount == 0:
                    win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    animCount += 1
                else:
                    animCount += 1
            else:
                if animCount == 0:
                    win.blit(self.jetpackRight_1[self.position], (self.x - 8 - 9, self.y))
                    win.blit(self.jetpackLeft_1[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                elif animCount == 2:
                    win.blit(self.jetpackRight_2[self.position], (self.x - 8 - 9, self.y))
                    win.blit(self.jetpackLeft_2[self.position], (self.x + width - 8, self.y))
                    animCount += 1
                else:
                    animCount += 1
        elif self.position >= 10 and jetpack_flag:
            if left_fall:
                self.y += S
                S += 5
                win.blit(self.jetpackFallLeft, (x_fall, self.y))
            elif right_fall:
                self.y += S
                S += 5
                win.blit(self.jetpackFallRight, (x_fall - width - 9, self.y))
            else:
                self.y += S
                S += 5
                win.blit(self.jetpackFallLeft, (x_fall + width, self.y))
                win.blit(self.jetpackFallRight, (x_fall - 26, self.y))
        if self.y > 512 - 32:
            jetpack_flag = False

    def catchJetpack(self):
        win.blit(self.jetpackCatch, (self.x + width - 8, self.y))