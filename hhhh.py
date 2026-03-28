import pygame
import pytmx
import pyscroll


from map import Game

if __name__ == '__main__':
    pygame.init()
    map = Game()
    map.run()