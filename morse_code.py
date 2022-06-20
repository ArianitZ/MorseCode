import sys
import pygame
from pygame.locals import *
from constants import MORSE_CODE


def initialize_pygame(width, height) -> pygame.Surface:
    pygame.init()
    displaySurface = pygame.display.set_mode((width, height))

    return displaySurface


def get_start_screen():
    pass


def terminate():
    pygame.quit()
    sys.exit()


def main():
    window_height = 600
    window_width = 960
    initialize_pygame(window_width, window_height)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()


if __name__ == "__main__":
    main()
