import pygame
from Game import *
pygame.init()


def main():
    global my_game
    my_game = Game()
    my_game.run(my_game)


if __name__ == '__main__':
    main()

