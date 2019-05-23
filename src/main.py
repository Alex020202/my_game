import pygame
from Game import Game
pygame.init()


def main():
    global my_game
    my_game = Game()
    my_game.run()


if __name__ == '__main__':
    main()

