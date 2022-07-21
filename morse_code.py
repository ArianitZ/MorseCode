import sys
import pygame
from pygame.locals import *
from constants import MAXIMUM_WORD_LENGTH, MORSE_CODE, FPS, DOT_RADIUS, DASH_DIMENSIONS
from typing import Tuple, List
from word_handler import WordHandler
from button import Button
from utilities import Color, Point
import time


def initialize_pygame(
    width: int, height: int, caption: str
) -> Tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize pygame and create a pygame display surface and a clock for controlling the FPS

    Args:
        width (int): width of display surface
        height (int): height of display surface
        caption (str): caption of display surface

    Returns:
        Tuple[pygame.Surface, pygame.time.Clock]: display surface and main clock controlling the FPS
    """
    pygame.init()
    fps_clock = pygame.time.Clock()
    displaySurface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)

    return displaySurface, fps_clock


def create_text(
    text: str, font_size: int, coordinates: Tuple[int, int], color: Color = Color(0, 0, 0)
) -> Tuple[pygame.Surface, pygame.Rect]:
    """Creates a surface and rectangle for displaying text

    Args:
        text (str): The desired text.
        font_size (int): Size of text.
        coordinates (Tuple[int, int]): Where the text is supposed to be placed.
        color (Color, optional): Color of text. Defaults to Color(255, 255, 255).

    Returns:
        Tuple[pygame.Surface, pygame.Rect]: Text surface and rectangle
    """
    font = pygame.font.Font("freesansbold.ttf", font_size)
    text_surface = font.render(text, True, color)

    text_rectangle = text_surface.get_rect()
    text_rectangle.center = coordinates

    return text_surface, text_rectangle


def get_midpoint(display: pygame.Surface) -> Point[int, int]:
    """Returns the middle point of a surface.

    Args:
        display (pygame.Surface): Desired surface to get midpoint for.

    Returns:
        Point[int, int]: The midpoint of the display
    """
    return Point(display.get_width() // 2, display.get_height() // 2)


def check_keyup_event() -> bool:
    """Returns true or false depending on whether a keyup event is found or not.

    Returns:
        bool: Returns true if a keyup event is found, false otherwise.
    """
    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
            terminate()
        elif event.type == KEYUP:
            return True
    return False


def terminate() -> None:
    """Convenience function for terminating the program."""
    pygame.quit()
    sys.exit()


def use_start_screen(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    background_color: Color = Color(255, 0, 0),
) -> None:
    """Creates the first screen that the user interacts with.
    This screen is continously shown until the user presses a key to move forward to the
    instruction screen.

    Args:
        display_surface (pygame.Surface): Main game surface.
        fps_clock (pygame.time.Clock): Main game clock.
        background_color (Color, optional): Start screen color. Defaults to Color(255, 0, 0).
    """
    midpoint_display_surface = get_midpoint(display_surface)
    header_coorindates = (
        midpoint_display_surface.x,
        midpoint_display_surface.y - 20,
    )
    paragraph_coordinates = (
        midpoint_display_surface.x,
        midpoint_display_surface.y + 20,
    )

    header_surface, header_rect = create_text("Morse Code", 32, header_coorindates)
    paragraph_surface, paragraph_rect = create_text(
        "Press any key to start", 24, paragraph_coordinates
    )

    while True:
        display_surface.fill(background_color)

        display_surface.blit(header_surface, header_rect)
        display_surface.blit(paragraph_surface, paragraph_rect)

        if check_keyup_event():
            return

        pygame.display.update()
        fps_clock.tick(FPS)


def use_instructions_screen(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    background_color: Color = Color(192, 192, 192),
) -> None:
    """Displays the instructions needed for playing the game.

    Args:
        display_surface (pygame.Surface): main game surface.
        fps_clock (pygame.time.Clock): main game clock.
        background_color (Color, optional): background color of the screen. Defaults to Color(192, 192, 192) (gray).
    """
    instructions = [
        "Instructions",
        "1. Each letter in a word is represented by a sequence of dots and dashses.",
        "2. Your mission is to enter the correct letter for each sequence of dots & dashses.",
        "3. You have five life points, each time you enter the incorrect letter a life point is lost.",
    ]
    midpoint_display_surface = get_midpoint(display_surface)

    gap_size = 20
    text_objects = []
    for i, instruction in enumerate(instructions):
        coordinates = (
            midpoint_display_surface.x,
            midpoint_display_surface.y + i * gap_size,
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


def calculate_sequence_positions(sequence: str, interval: Point[int, int]) -> List[int]:
    """Derive an evenly distributed list of positions for elements in a sequence

    Args:
        sequence (str): String consisting of dots & dashses.
        interval (Point[int, int]): end points of an interval.

    Returns:
        List[int]: An evenly distributed list of positions for the elements in the sequence.
    """
    interval_length = interval.y - interval.x
    n_sections = len(sequence)
    section_length = interval_length // n_sections

    sections = []
    for i in range(n_sections):
        section = (
            interval.x + i * section_length,
            interval.x + (i + 1) * section_length,
        )
        sections.append(section)

    sequence_positions = []
    for section in sections:
        section_mid_point = (section[1] - section[0]) // 2
        sequence_position = section[0] + section_mid_point
        sequence_positions.append(sequence_position)

    return sequence_positions


def draw_morse_code(display_surface: pygame.Surface, letter: str) -> None:
    """Draws the morse code representation of a letter onto a surface

    Args:
        display_surface (pygame.Surface): main game surface.
        letter (str): self-explanatory.
    """
    sequence = MORSE_CODE[letter.upper()]
    # Offset for one side
    x_offset = int(display_surface.get_width() * 0.3)
    x_interval = Point(x_offset, display_surface.get_width() - x_offset)

    x_positions = calculate_sequence_positions(sequence, x_interval)
    y_pos = display_surface.get_height() // 3
    for i, encoding in enumerate(sequence):
        x_pos = x_positions[i]
        if encoding == ".":
            pygame.draw.circle(display_surface, "black", (x_pos, y_pos), DOT_RADIUS)
        elif encoding == "-":
            pygame.draw.rect(
                display_surface, "black", (x_pos, y_pos, DASH_DIMENSIONS[0], DASH_DIMENSIONS[1])
            )


def draw_text(text: str, surface: pygame.Surface, position: Point, font_size: int = 128) -> None:
    """Creates a surface and rectangle for the provided text and blits them onto a surface.

    Args:
        text (str): text to display on the given surface.
        surface (pygame.Surface): any pygame surface.
        position (Point): where to display the text on the surface.
        font_size (int, optional): text size. Defaults to 128.
    """
    text_surf, text_rect = create_text(text, font_size, position)
    surface.blit(text_surf, text_rect)


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
    """Draws the current score of the player.

    Args:
        display_surface (pygame.Surface): main game surface.
        score (int): current score of the player.
        position (Point): where to draw the score.
        font_size (int, optional): size of the text. Defaults to 20.
    """
    score_msg = f"Score: {score}"
    score_surf, score_rect = create_text(score_msg, font_size=font_size, coordinates=position)
    display_surface.blit(score_surf, score_rect)


def draw_guessed_letters(
    display_surface: pygame.Surface, letters: List[str], font_size: int = 16
) -> None:
    """Draws all the guessed letters onto a surface.

    Args:
        display_surface (pygame.Surface): main game surface.
        letters (List[str]): sequence of letters to draw on the surface.
        font_size (int, optional): text size. Defaults to 16.
    """
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


def draw_life_bar(display_surface: pygame.Surface, lives: int, max_lives: int = 5) -> None:
    """Draws life bars onto a screen. Red life bars are used for the remaining lives while
    transparent life bars are used for lives lost.

    Args:
        display_surface (pygame.Surface): main game surface
        lives (int): current number of life points
        max_lives (int, optional): maximum life points. Defaults to 5.
    """
    bar_size = Point(40, 10)
    gap_size = 2
    start_position = Point(
        display_surface.get_width() // 30 * 1,
        display_surface.get_height() // 30 * 1 + max_lives * (bar_size.y + gap_size),
    )
    red = Color(255, 0, 0)  # TODO: move this to constants.py
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
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    background_color: Color = Color(255, 255, 255),
) -> None:
    """Main game screen, initializes all needed variables and runs the main game loop.

    Args:
        display_surface (pygame.Surface): main game surface.
        fps_clock (pygame.time.Clock): main game clock.
        background_color (Color, optional): background color of screen. Defaults to Color(255, 255, 255) (white).
    """
    word_handler = WordHandler(max_size=MAXIMUM_WORD_LENGTH)
    word = word_handler.fetch_new_word().upper()
    # TODO find a better way to fetch new characters
    letter_index = 0  # word[0]

    score = 0
    score_y = display_surface.get_height() // 10 * 1
    score_x = display_surface.get_width() // 10 * 9
    score_position = Point(score_x, score_y)

    guessed_letters = list()
    guessed_letter = ""
    guessed_letter_position = Point(
        display_surface.get_width() // 2, display_surface.get_height() // 4 * 3
    )

    cheat_button_position_y = display_surface.get_height() // 12 * 10
    cheat_button_position_x = display_surface.get_width() // 12 * 10
    cheat_button = Button("Cheat", (cheat_button_position_x, cheat_button_position_y), 30)
    use_cheat_screen = False

    lives = 5

    red_color = Color(255, 0, 0)  # TODO move these to constants.py
    green_color = Color(0, 255, 0)

    while True:
        letter = word[letter_index]

        display_surface.fill(background_color)
        draw_morse_code(display_surface, letter)
        draw_score(display_surface, score, score_position)
        draw_guessed_letters(display_surface, guessed_letters)
        draw_life_bar(display_surface, lives)
        cheat_button.draw_button(display_surface)

        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYUP and event.unicode.isalpha():
                guessed_letter = event.unicode.upper()
            elif cheat_button.isClicked(event):
                use_cheat_screen = True

        draw_text(guessed_letter, display_surface, guessed_letter_position)
        if use_cheat_screen:
            draw_cheat_screen(display_surface, fps_clock, letter)
            use_cheat_screen = False
        if guessed_letter == letter:
            draw_blinking_surface(display_surface, fps_clock, green_color, 3)
            guessed_letters = list()
            guessed_letter = ""
            score += 1
            letter_index += 1
            if letter_index >= len(word):
                word = word_handler.fetch_new_word().upper()
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


def draw_cheat_screen(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    current_letter: str,
    background_color: Color = Color(255, 0, 0),
) -> None:
    """Draws a cheat screen where the current letter is shown to the player.

    Args:
        display_surface (pygame.Surface): main game surface
        fps_clock (pygame.time.Clock): main game clock
        current_letter (str): current letter, will be shown to the player
        background_color (Color, optional): background color of the screen. Defaults to Color(255, 0, 0) (red).
    """
    display_coordinates = Point(display_surface.get_width() // 2, display_surface.get_height() // 3)
    cheat_text_surf, cheat_text_rect = create_text("Cheating Mode", 60, display_coordinates)
    letter_surf, letter_rect = create_text(
        f"Current letter: {current_letter}", 30, (display_coordinates.x, display_coordinates.y * 2)
    )

    display_surface.fill(background_color)
    display_surface.blit(cheat_text_surf, cheat_text_rect)
    display_surface.blit(letter_surf, letter_rect)

    pygame.display.update()
    fps_clock.tick(FPS)
    time.sleep(1)


def use_gameover_screen(
    display_surface: pygame.Surface,
    fps_clock: pygame.time.Clock,
    current_word: str,
    score: int,
    background_color: Color = (0, 0, 0),
    text_color: Color = (255, 255, 255),
) -> None:
    """Displays the current word as well as the final score for the player.

    Args:
        display_surface (pygame.Surface): main game surface.
        fps_clock (pygame.time.Clock): main game clock.
        current_word (str): the current word.
        score (int): the final score for the player.
        background_color (Color, optional): background color of the screen. Defaults to (0, 0, 0) (black).
        text_color (Color, optional): text color. Defaults to (255, 255, 255) (white).
    """

    display_position = Point(display_surface.get_width() // 2, display_surface.get_height() // 4)
    gameover_surf, gameover_rect = create_text(
        "Game Over", 60, (display_position.x, display_position.y), text_color
    )
    current_word_surf, current_word_rect = create_text(
        f"The correct word was: {current_word}",
        30,
        (display_position.x, display_position.y * 2),
        text_color,
    )
    score_surf, score_rect = create_text(
        f"Score: {score}", 30, (display_position.x, display_position.y * 3), text_color
    )

    time.sleep(
        0.5
    )  # Wait for a short period since the user might have pressed a key just after the last guess
    # Empty event queue before showing game over screen
    pygame.event.get()
    while True:
        if check_keyup_event():
            return
        display_surface.fill(background_color)
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
