import sys
from venv import create
import pygame
from pygame.locals import *
from constants import MORSE_CODE, FPS, DOT_RADIUS, DASH_DIMENSIONS
from typing import Tuple, List

# TODO Make DOT_RADIUS & DASH_DIMENSIONS NamedTuples
def initialize_pygame(
    width: int, height: int, caption: str
) -> Tuple[pygame.Surface, pygame.time.Clock]:
    pygame.init()
    fps_clock = pygame.time.Clock()
    displaySurface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)

    return displaySurface, fps_clock


def create_text(
    msg: str, font_size: int, coordinates: Tuple[int, int], color: str = "black"
) -> Tuple[pygame.Surface, pygame.Rect]:
    font = pygame.font.Font("freesansbold.ttf", font_size)
    text = font.render(msg, True, color)

    text_rect = text.get_rect()
    text_rect.center = coordinates

    return text, text_rect


def get_midpoint(display: pygame.Surface) -> Tuple[int, int]:
    return (display.get_width() // 2, display.get_height() // 2)


def check_keyup_event() -> bool:
    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
            terminate()
        elif event.type == KEYUP:
            return True
    return False


def use_start_screen(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    background_color: str = "red",
) -> None:
    middle_of_display_surface = get_midpoint(display_surface)
    header_coorindates = (
        middle_of_display_surface[0],
        middle_of_display_surface[1] - 20,
    )
    paragraph_coordinates = (
        middle_of_display_surface[0],
        middle_of_display_surface[1] + 20,
    )

    header_text, header_rect = create_text("Morse Code", 32, header_coorindates)
    paragraph_text, paragraph_rect = create_text(
        "Press any key to start", 24, paragraph_coordinates
    )

    while True:
        display_surface.fill(background_color)

        display_surface.blit(header_text, header_rect)
        display_surface.blit(paragraph_text, paragraph_rect)

        if check_keyup_event():
            return

        pygame.display.update()
        fps_clock.tick(FPS)


def terminate() -> None:
    pygame.quit()
    sys.exit()


def get_next_word() -> str:
    return "SOS"


# TODO find a better name for this fcn
def calculate_sequence_positions(sequence: str, x_max) -> int:
    # TODO Fix so that the sequence is in the center
    n_gaps = len(sequence) + 2
    return x_max // n_gaps


def draw_morse_code(display_surface: pygame.Surface, letter: str) -> None:
    sequence = MORSE_CODE[letter]

    gap_size = calculate_sequence_positions(sequence, display_surface.get_width())
    y_pos = display_surface.get_height() // 2
    for i, char in enumerate(sequence):
        x_pos = gap_size * (i + 2)
        print(x_pos, y_pos)
        if char == ".":
            pygame.draw.circle(display_surface, "black", (x_pos, y_pos), DOT_RADIUS)
        elif char == "-":
            pygame.draw.rect(display_surface, "black", (x_pos, y_pos))


def use_instructions_screen(
    display_surface: pygame.Surface, fps_clock: pygame.time.Clock, background_color: str = "gray"
) -> None:
    instructions = [
        "Instructions",
        "1. Each letter in a word is represented by a sequence of dots and dashses.",
        "2. Your mission is to enter the correct letter for each sequence of dots & dashses.",
    ]
    midpoint_display_surface = get_midpoint(display_surface)

    gap_size = 20
    text_objects = []
    for i, instruction in enumerate(instructions):
        coordinates = (
            midpoint_display_surface[0],
            midpoint_display_surface[1] + i * gap_size,
        )
        text_objects.append(create_text(instruction, 20, coordinates))

    while True:
        display_surface.fill(background_color)
        for text, text_rect in text_objects:
            display_surface.blit(text, text_rect)
        if check_keyup_event():
            return
        pygame.display.update()
        fps_clock.tick()


def use_game_screen(display_surface, fps_clock, background_color="white") -> None:
    next_word = get_next_word()
    next_letter = next_word[0]

    while True:
        display_surface.fill(background_color)
        draw_morse_code(display_surface, next_letter)
        if check_keyup_event():
            return
        pygame.display.update()
        fps_clock.tick()


def main():
    window_height = 600
    window_width = 960
    caption = "Morse Code"
    display_surface, fps_clock = initialize_pygame(window_width, window_height, caption)

    use_start_screen(display_surface, fps_clock)
    use_instructions_screen(display_surface, fps_clock)
    use_game_screen(display_surface, fps_clock)


if __name__ == "__main__":
    main()
