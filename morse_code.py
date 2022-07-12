import sys
import pygame
from pygame.locals import *
from constants import MAXIMUM_WORD_LENGTH, MORSE_CODE, FPS, DOT_RADIUS, DASH_DIMENSIONS
from typing import Tuple, List, NamedTuple
from word_handler import WordHandler
import time

# TODO Add documentation to each function. Install docstring


class Color(NamedTuple):
    r: str
    g: str
    b: str


class Point(NamedTuple):
    x: int
    y: int


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


def calculate_sequence_positions(sequence: str, interval: Tuple[int, int]) -> List[int]:
    interval_length = interval[1] - interval[0]
    n_sections = len(sequence)
    section_length = interval_length // n_sections

    sections = []
    for i in range(n_sections):
        section = (
            interval[0] + i * section_length,
            interval[0] + (i + 1) * section_length,
        )
        sections.append(section)

    sequence_positions = []
    for section in sections:
        section_mid_point = (section[1] - section[0]) // 2
        sequence_position = section[0] + section_mid_point
        sequence_positions.append(sequence_position)

    return sequence_positions


def draw_morse_code(display_surface: pygame.Surface, letter: str) -> None:
    sequence = MORSE_CODE[letter.upper()]
    # Offset for one side
    x_offset = int(display_surface.get_width() * 0.3)
    x_interval = x_offset, display_surface.get_width() - x_offset

    x_positions = calculate_sequence_positions(sequence, x_interval)
    y_pos = display_surface.get_height() // 3
    for i, char in enumerate(sequence):
        x_pos = x_positions[i]
        if char == ".":
            pygame.draw.circle(display_surface, "black", (x_pos, y_pos), DOT_RADIUS)
        elif char == "-":
            pygame.draw.rect(
                display_surface, "black", (x_pos, y_pos, DASH_DIMENSIONS[0], DASH_DIMENSIONS[1])
            )


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
        fps_clock.tick(FPS)


def draw_letter(letter: str, display_surface: pygame.Surface, fontsize: int = 128) -> None:
    x = display_surface.get_width() // 2
    y = display_surface.get_height() // 4 * 3
    text_surf, text_rect = create_text(letter, fontsize, (x, y))

    display_surface.blit(text_surf, text_rect)


# TODO make this function a bit better, move _draw_continuous_hue outside the fcn?
def draw_blinking_surface(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    blinking_color: Color,
    number_of_blinks: int,
    animation_speed: int = 75,
) -> None:
    original_surface = display_surface.copy()

    def _draw_continuous_hue(start: int, end: int, step: int, animation_speed: int, color) -> None:
        for alpha in range(start, end, step * animation_speed):
            display_surface.blit(original_surface, (0, 0))
            flash_surface.fill((color.r, color.g, color.b, alpha)),
            display_surface.blit(flash_surface, (0, 0))
            pygame.display.update()
            fps_clock.tick(FPS)

    flash_surface = display_surface.convert_alpha()
    display_surface.blit(original_surface, (0, 0))
    for i in range(number_of_blinks):
        for (start, end, step) in ((0, 255, 1), (255, 0, -1)):
            _draw_continuous_hue(start, end, step, animation_speed, blinking_color)
    display_surface.blit(original_surface, (0, 0))


def draw_score(
    display_surface: pygame.Surface, score: int, position: Point, font_size: int = 20
) -> None:
    score_msg = f"Score: {score}"
    score_surf, score_rect = create_text(score_msg, font_size=font_size, coordinates=position)
    display_surface.blit(score_surf, score_rect)


def draw_guessed_letters(
    display_surface: pygame.Surface, letters: List[str], font_size: int = 16
) -> None:
    display_coords = Point(display_surface.get_width(), display_surface.get_height())
    start_pos = Point(display_coords.x // 10 * 1, display_coords.y // 10 * 8)
    max_x_pos = display_coords.x // 10 * 9
    gap_size = Point(0, 0)

    texts_to_print = ["Guesses:"] + letters
    for text in texts_to_print:
        text_position = Point(start_pos.x + gap_size.x, start_pos.y)
        if text_position.x > max_x_pos:
            text_position.y = start_pos.y + gap_size.y

        text_surf, text_rect = create_text(text, font_size, text_position)
        display_surface.blit(text_surf, text_rect)

        gap_size = Point(
            gap_size.x + text_surf.get_width() + 5, gap_size.y + text_surf.get_height() + 5
        )


# TODO make a nice border around the life bars
def draw_life_bar(display_surface: pygame.Surface, lives: int, max_lives: int = 5) -> None:
    bar_size = Point(40, 10)
    gap_size = 2
    start_position = Point(
        display_surface.get_width() // 30 * 1,
        display_surface.get_height() // 30 * 1 + max_lives * (bar_size.y + gap_size),
    )
    red = Color(255, 0, 0)
    black = Color(0, 0, 0)
    for i in range(max_lives):
        pygame.draw.rect(
            display_surface,
            black,
            (
                start_position.x,
                start_position.y - i * (bar_size.y + gap_size),
                bar_size.x,
                bar_size.y,
            ),
            1,
            2,
        )
    for i in range(lives):
        pygame.draw.rect(
            display_surface,
            red,
            (
                start_position.x,
                start_position.y - i * (bar_size.y + gap_size),
                bar_size.x,
                bar_size.y,
            ),
            0,
            2,
        )


# TODO: split this function into several parts
def use_game_screen(
    display_surface: pygame.Surface, fps_clock: pygame.time.Clock, background_color: str = "white"
) -> None:
    word_handler = WordHandler(max_size=MAXIMUM_WORD_LENGTH)
    word = word_handler.fetch_new_word().upper()
    letter_index = 0  # word[0]
    score = 0
    score_y = display_surface.get_height() // 10 * 1
    score_x = display_surface.get_width() // 10 * 9
    score_position = Point(score_x, score_y)

    guessed_letters = list()
    guessed_letter = ""

    lives = 5

    red_color = Color(255, 0, 0)
    green_color = Color(0, 255, 0)
    while True:
        letter = word[letter_index]
        display_surface.fill(background_color)
        draw_morse_code(display_surface, letter)
        draw_score(display_surface, score, score_position)
        draw_guessed_letters(display_surface, guessed_letters)
        draw_life_bar(display_surface, lives)

        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYUP and event.unicode.isalpha():
                guessed_letter = event.unicode.upper()
        draw_letter(guessed_letter, display_surface)
        if guessed_letter == letter:
            draw_blinking_surface(display_surface, fps_clock, green_color, 3)
            guessed_letters = list()
            guessed_letter = ""
            score += 1
            letter_index += 1
            if letter_index >= len(word):
                word = word_handler.fetch_new_word()
                letter_index = 0
        elif guessed_letter.isalpha():
            draw_blinking_surface(display_surface, fps_clock, red_color, 1, animation_speed=25)
            guessed_letters.append(guessed_letter)
            guessed_letter = ""
            lives -= 1

        if lives <= 0:
            use_gameover_screen(display_surface, fps_clock, word_handler.get_current_word(), score)
            score = 0
            lives = 5
            guessed_letters = list()
            word = word_handler.fetch_new_word()
            letter_index = 0

        pygame.display.update()
        fps_clock.tick(FPS)


# TODO: implement this function which saves the score of the player
def save_score():
    pass


def use_gameover_screen(
    display_surface: pygame.Surface, fps_clock: pygame.time.Clock, current_word: str, score: int
) -> None:
    black = Color(0, 0, 0)
    white = Color(255, 255, 255)

    display_position = Point(display_surface.get_width(), display_surface.get_height())
    gameover_surf, gameover_rect = create_text(
        "Game Over", 60, (display_position.x // 2, display_position.y // 4), white
    )
    current_word_surf, current_word_rect = create_text(
        f"The correct word was: {current_word}",
        30,
        (display_position.x // 2, display_position.y // 4 * 2),
        white,
    )
    score_surf, score_rect = create_text(
        f"Score: {score}", 30, (display_position.x // 2, display_position.y // 4 * 3), white
    )

    time.sleep(
        0.5
    )  # Wait for a short period since the user might have pressed key just after the last guess
    # Empty event queue before showing game over screen
    pygame.event.get()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYUP:
                return
        display_surface.fill(black)
        display_surface.blit(gameover_surf, gameover_rect)
        display_surface.blit(current_word_surf, current_word_rect)
        display_surface.blit(score_surf, score_rect)
        pygame.display.update()
        fps_clock.tick(FPS)


def main() -> None:
    window_height = 600
    window_width = 960
    caption = "Morse Code"
    display_surface, fps_clock = initialize_pygame(window_width, window_height, caption)

    use_start_screen(display_surface, fps_clock)
    use_instructions_screen(display_surface, fps_clock)
    use_game_screen(display_surface, fps_clock)

    return 0


if __name__ == "__main__":
    main()
