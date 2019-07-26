import pygame
import random
from Block import Block
from Hero import Hero
from Jetpack import *
import openpyxl


class Game:
    def __init__(self):
        self.win_width = 320
        self.win_height = 512
        self.win = pygame.display.set_mode((self.win_width, self.win_height + 64))

        pygame.display.set_caption("Doodle Jump")

        self.background = pygame.image.load("../assets/pictures/background_s.png")
        self.bottom = pygame.image.load("../assets/pictures/Bottom.png")

        self.button_play = [
            pygame.image.load("../assets/pictures/MainMenu/play.png"),
            pygame.image.load("../assets/pictures/MainMenu/play-on.png")
        ]

        self.button_scores = [
            pygame.image.load("../assets/pictures/MainMenu/scores.png"),
            pygame.image.load("../assets/pictures/MainMenu/scores-on.png")
        ]

        self.button_cancel = [
            pygame.image.load("../assets/pictures/MainMenu/cancel.png"),
            pygame.image.load("../assets/pictures/MainMenu/cancel-on.png")
        ]


        self.buttons_width = 110
        self.buttons_height = 40
        self.button_play_x = self.win_width / 2 - self.buttons_width / 2
        self.button_play_y = 100
        self.button_scores_x = self.win_width / 2 - self.buttons_width / 2
        self.button_scores_y = 200
        self.button_cancel_x = self.win_width / 2 - self.buttons_width / 2
        self.button_cancel_y = 400
        self.button_cancel_stage = 0

        self.y_loc = 450  # position of spawning blocks
        self.Blocks_list = []  # list of active blocks
        self.Blocks_list.append(Block(150, 501, False, self))
        for i in range(10):
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))
            self.y_loc -= random.randrange(50, 150)
        self.clock = pygame.time.Clock()  # fps
        self.score = 0  # player's score
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)  # font
        self.textsurface = None  # first message
        self.music = 1  # number of playing music
        self.is_running = True  # if main cycle is going
        self.change_y_position = 0  # coordinates changing of objects' position
        self.Hero = Hero(self)
        self.key = 0  # number of music
        self.jetpack_flag = False
        self.jetpack_begin = None
        self.is_jet_on_block = False
        self.Jetpack = None
        self.game_stage = "main menu"
        self.button_play_stage = 0
        self.button_scores_stage = 0
        self.highscores = "../assets/highscores.xlsx"
        self.list_of_scores = []
        self.first_time_scores_opening = True
        self.first_time_menu_opening = True
        self.adding_new_score = True

        self.values_from_column_A = []
        self.values_from_column_B = []
        self.new_score = str()
        self.FPS = 30

    def create_block(self):
        self.y_loc = self.Blocks_list[len(self.Blocks_list) - 1].y - random.randrange(50, 200)
        if self.score // 1000 % 30 == 0 and self.score > 10000:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        elif random.randrange(30 - self.score // 1000 % 29) == 0:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, True, self))
        else:
            self.Blocks_list.append(Block(random.randrange(320 - 40), self.y_loc, False, self))

    def touch_block(self):
        for block in self.Blocks_list:
            if (self.Hero.right_side >= block.x and self.Hero.x <= block.right_side) and self.Hero.next_legs_position \
                    >= block.y >= self.Hero.legs_position:
                self.Hero.push_off(block)
                if block.check_del:
                    self.Blocks_list.remove(block)
                    self.create_block()

    def game_over(self):
        if self.music == 0:
            self.play_music(0)
            self.music += 1
        pygame.display.update()
        self.win.blit(self.background, (0, 0))

        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        if self.score < self.values_from_column_A[9]:
            self.textsurface = self.myfont.render('ГЕЙМ ОВЕР', False, (0, 0, 0))  # first message
            self.win.blit(self.textsurface, (120, 100))
            self.textsurface = self.myfont.render('ХА-ХА-ХА'.format(int(self.score)), False, (0, 0, 0))
            self.win.blit(self.textsurface, (120, 150))
            self.textsurface = self.myfont.render('ВЫ СЛИШКОМ ПЛОХО ИГРАЛИ!\n СЧЕТ:{}'.format(int(self.score)), False,
                                                  (0, 0, 0))
            self.win.blit(self.textsurface, (0, 200))
            self.textsurface = self.myfont.render('СЧЕТ:{}'.format(int(self.score)), False, (0, 0, 0))
            self.win.blit(self.textsurface, (120, 250))
            self.win.blit(self.button_cancel[self.button_cancel_stage], (self.button_cancel_x, self.button_cancel_y))

        else:
            self.textsurface = self.myfont.render("ВЫ ВОШЛИ В ТОП-10!", False, (0, 0, 0))
            self.win.blit(self.textsurface, (60, 100))
            self.textsurface = self.myfont.render("Ваш счет:{}".format(int(self.score)), False, (0, 0, 0))
            self.win.blit(self.textsurface, (100, 140))
            self.textsurface = self.myfont.render("Ваше имя: ", False, (0, 0, 0))
            self.win.blit(self.textsurface, (120, 200))
            self.textsurface = self.myfont.render(self.new_score, False, (0, 0, 0))
            self.win.blit(self.textsurface, (120, 230))
            if self.adding_new_score:
                self.adding_scores()
            else:
                self.scores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.__init__()
            elif event.type == pygame.MOUSEMOTION:
                if self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.button_cancel_stage = 1
                else:
                    self.button_cancel_stage = 0

    def play_music(self, key):
        if key != 0:
            self.key = key % 5 + 1
        else:
            self.key = 0
        if self.key == 0 and self.music == 0:
            pygame.mixer.music.load("../assets/music/strashnye-zvuki-d-yavol-skiy-smeh.mp3")
        elif self.key == 1:
            pygame.mixer.music.load("../assets/music/coldplay_feat_beyonce_-_hymn_for_the_weekend_(zf.fm).mp3")
        elif self.key == 2:
            pygame.mixer.music.load("../assets/music/Celldweller - Frozen.mp3")
        elif self.key == 3:
            pygame.mixer.music.load("../assets/music/teddybears_sthlm_and_mad_cobra_-_cobrastyle_(zaycev.net).mp3")
        elif self.key == 4:
            pygame.mixer.music.load("../assets/music/ylvis_-_what_does_the_fox_say_(zaycev.net).mp3")
        elif self.key == 5:
            pygame.mixer.music.load("../assets/music/tiesto__sevenn_-_boom_2017_(zf.fm).mp3")
        pygame.mixer.music.play()
        self.music += 1

    def draw_win(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.background, (0, 0))
        self.win.blit(self.bottom, (0, 511))
        self.textsurface = self.myfont.render('Score: {}'.format(int(self.score)), False, (0, 0, 0))
        self.win.blit(self.textsurface, (0, 0))
        for block in self.Blocks_list:
            block.draw()
        self.Hero.draw()
        self.Hero.draw_slot()
        if self.is_jet_on_block:
            self.Jetpack.catch_jetpack()
        pygame.display.update()

    def main_menu(self):
        if self.first_time_menu_opening:
            self.reading_scores()
            self.first_time_menu_opening = False
        self.win.fill((0, 0, 0))
        self.win.blit(self.background, (0, 0))
        self.win.blit(self.bottom, (0, 511))
        self.win.blit(self.button_play[self.button_play_stage], (self.button_play_x, self.button_play_y))
        self.win.blit(self.button_scores[self.button_scores_stage], (self.button_scores_x, self.button_scores_y))
        self.win.blit(self.button_cancel[self.button_cancel_stage], (self.button_cancel_x, self.button_cancel_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_play_x < event.pos[0] < self.button_play_x + self.buttons_width \
                        and self.button_play_y < event.pos[1] < self.button_play_y + self.buttons_height:
                    self.game_stage = "play"
                elif event.button == 1 and self.button_scores_x < event.pos[0] < self.button_scores_x + self.buttons_width \
                        and self.button_scores_y < event.pos[1] < self.button_scores_y + self.buttons_height:
                    self.game_stage = "scores"
                elif event.button == 1 and self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.is_running = False

            elif event.type == pygame.MOUSEMOTION:
                if self.button_play_x < event.pos[0] < self.button_play_x + self.buttons_width \
                        and self.button_play_y < event.pos[1] < self.button_play_y + self.buttons_height:
                    self.button_play_stage = 1
                else:
                    self.button_play_stage = 0

                if self.button_scores_x < event.pos[0] < self.button_scores_x + self.buttons_width \
                        and self.button_scores_y < event.pos[1] < self.button_scores_y + self.buttons_height:
                    self.button_scores_stage = 1
                else:
                    self.button_scores_stage = 0

                if self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.button_cancel_stage = 1
                else:
                    self.button_cancel_stage = 0

        pygame.display.update()

    def scores(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.background, (0, 0))
        self.win.blit(self.bottom, (0, 511))
        if self.first_time_scores_opening:
            self.sorting_scores()
            print(self.values_from_column_A, self.values_from_column_B)
            self.first_time_scores_opening = False
        for i in range(10):
            self.textsurface = self.myfont.render(
                str(i + 1) + ". " + str(self.values_from_column_A[i]) + " : " + self.values_from_column_B[i], False,
                (0, 0, 0))
            self.win.blit(self.textsurface, (100, 100 + i * 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.__init__()
            elif event.type == pygame.MOUSEMOTION:
                if self.button_cancel_x < event.pos[0] < self.button_cancel_x + self.buttons_width \
                        and self.button_cancel_y < event.pos[1] < self.button_cancel_y + self.buttons_height:
                    self.button_cancel_stage = 1
                else:
                    self.button_cancel_stage = 0
        self.win.blit(self.button_cancel[self.button_cancel_stage], (self.button_cancel_x, self.button_cancel_y))

        pygame.display.update()

    def reading_scores(self):
        self.excel_highscores = openpyxl.load_workbook(filename=self.highscores)
        self.sheet = self.excel_highscores['Test']
        for i in range(10):
            self.values_from_column_A.append(self.sheet['A{}'.format(i + 2)].value)
            self.values_from_column_B.append(self.sheet['B{}'.format(i + 2)].value)

    def sorting_scores(self):
        for i in range(len(self.values_from_column_A) - 1):
            for j in range(len(self.values_from_column_A) - 1):
                if self.values_from_column_A[j] < self.values_from_column_A[j + 1]:
                    A = self.values_from_column_A[j + 1]
                    self.values_from_column_A[j + 1] = self.values_from_column_A[j]
                    self.values_from_column_A[j] = A
                    B = self.values_from_column_B[j + 1]
                    self.values_from_column_B[j + 1] = self.values_from_column_B[j]
                    self.values_from_column_B[j] = B
        for i in range(10):
            self.sheet['A{}'.format(i + 2)] = self.values_from_column_A[i]
            self.sheet['B{}'.format(i + 2)] = self.values_from_column_B[i]
        self.excel_highscores.save(self.highscores)

    def adding_scores(self):
        self.values_from_column_A[9] = int(self.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.values_from_column_B[9] = self.new_score
                    self.sorting_scores()
                    self.adding_new_score = False
                elif event.key == pygame.K_BACKSPACE:
                    self.new_score = self.new_score[:-1]
                else:
                    self.new_score += event.unicode

    def changing_difficulty(self):
        if 40000 >= self.score >= 10000:
            self.FPS = 30 + self.score // 1000 - 10
        elif self.score > 40000:
            self.FPS = 60
        else:
            self.FPS = 30

    def spawning_jetpack(self):
        if 0 < self.score % 1000 < 50 < self.score and not self.is_jet_on_block and self.Hero.slot is None:
            self.is_jet_on_block = True
            self.Jetpack = Jetpack(self)

    def catching_jetpack(self):
        if self.is_jet_on_block and (
                self.Jetpack.y < self.Hero.y < self.Jetpack.y + 36 or self.Jetpack.y < self.Hero.y + self.Hero.height < self.Jetpack.y + 36) and (
                self.Hero.x + self.Hero.width > self.Jetpack.x > self.Hero.x or self.Hero.x < self.Jetpack.x + 26 < self.Hero.x + self.Hero.width):
            self.Hero.slot = self.Jetpack
            self.is_jet_on_block = False
            self.jetpack_flag = True
            self.Jetpack.jetpack_begin = self.score

    def changing_coordinates(self):
        if not self.Hero.is_jump:
            self.Hero.is_jump = True
        else:
            if self.Hero.next_legs_position < self.win_height:
                self.change_y_position = self.Hero.objects_falling()
                self.score += self.change_y_position
            else:
                self.game_stage = "game over"
                self.music = 0

            if self.is_jet_on_block:
                self.Jetpack.y += self.change_y_position
                if self.Jetpack.y > self.win_height:
                    self.is_jet_on_block = False
                    self.Jetpack = None

            for block in self.Blocks_list:
                block.y += self.change_y_position
                if block.y > self.win_height:
                    self.Blocks_list.remove(block)
                    self.create_block()

    def run(self):
        while self.is_running:
            if self.game_stage == "main menu":
                self.main_menu()

            elif self.game_stage == "scores":
                self.scores()

            elif self.game_stage == "play":
                self.changing_difficulty()
                self.clock.tick(self.FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.play_music(self.music)

                self.spawning_jetpack()
                self.catching_jetpack()
                if self.jetpack_flag:
                    self.Jetpack.counting_position()
                if self.Jetpack is not None and not self.jetpack_flag and not self.is_jet_on_block:
                    self.Jetpack = None

                self.Hero.move()

                self.changing_coordinates()

                self.Hero.change_variables()
                self.touch_block()
                self.draw_win()

            elif self.game_stage == "game over":
                self.game_over()

        pygame.quit()
