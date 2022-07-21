import pygame
from pygame.locals import MOUSEBUTTONUP
from typing import Tuple
from utilities import Point


class Button:
    """Class used for creating clickable buttons"""

    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        font_size: int = 40,
        offset: int = 5,
        shadow_offset: int = 3,
        button_color: Tuple[int, int, int] = (210, 0, 0),
        button_shadow_color: Tuple[int, int, int] = (100, 0, 0),
    ) -> None:
        """Create a button with a specified text, size, position and color.

        Args:
            text (str): Button text
            position (Tuple[int, int]): Position of button in a pygame surface
            font_size (int, optional): Font size of button text. Defaults to 40.
            offset (int, optional): Offset from the text surface. Defaults to 5.
            shadow_offset (int, optional): Number of pixels to offset the shadow effect. Defaults to 3.
            button_color (Tuple[int, int, int], optional): Color of the button. Defaults to (210, 0, 0).
            button_shadow_color (Tuple[int, int, int], optional): Color of the shadow. Defaults to (100, 0, 0).
        """
        self.button_text = text
        self.x, self.y = position
        self.font_size = font_size
        self.offset = offset
        self.shadow_offset = shadow_offset
        self.button_color = button_color
        self.button_shadow_color = button_shadow_color
        self.button_position = Point(self.x - self.offset, self.y - self.offset)
        self.create_button()

    def create_button(self) -> None:
        """Creates a button consisting of three pygame surfaces & rectangles: one for the text,
        one for the background and one for the background shadow effect.
        """

        # Text surface & rectangle
        font = pygame.font.Font("freesansbold.ttf", self.font_size)
        self.text_surface = font.render(self.button_text, True, "black")
        self.text_rectangle = self.text_surface.get_rect()
        self.text_rectangle.topleft = (self.x, self.y)
        text_dimensions = Point(self.text_surface.get_width(), self.text_surface.get_height())

        # Button surface & rectangle
        button_dimensions = Point(
            text_dimensions.x + 2 * self.offset, text_dimensions.y + 2 * self.offset
        )
        self.background_surface = pygame.Surface(
            (button_dimensions.x, button_dimensions.y), pygame.SRCALPHA
        )
        self.background_rectangle = pygame.draw.rect(
            self.background_surface,
            self.button_color,
            (
                0,
                0,
                button_dimensions.x,
                button_dimensions.y,
            ),
            0,
            5,
        )

        # Shadow effect surface & rectangle
        self.background_shadow_surface = pygame.Surface(
            (
                button_dimensions.x + self.shadow_offset,
                button_dimensions.y + self.shadow_offset,
            ),
            pygame.SRCALPHA,  # Enable alpha (makes the surface transparent)
        )
        self.background_shadow_rectangle = pygame.draw.rect(
            self.background_shadow_surface,
            self.button_shadow_color,
            (
                0,
                0,
                button_dimensions.x + self.shadow_offset,
                button_dimensions.y + self.shadow_offset,
            ),
            0,
            5,
        )

    def draw_button(self, display_surface: pygame.Surface) -> None:
        """Draws a button by blitting three different surfaces onto a given display surface.

        Args:
            display_surface (pygame.Surface): The surface the button is supposed to be drawn onto.
        """
        display_surface.blit(self.background_shadow_surface, self.button_position)
        display_surface.blit(self.background_surface, self.button_position)
        display_surface.blit(self.text_surface, self.text_rectangle)

    def isClicked(self, event: pygame.event.Event) -> bool:
        """Checks if the button has been clicked

        Args:
            event (pygame.event.Event): Any pygame event.

        Returns:
            bool: True if the button has been clicked, false otherwise.
        """
        if event.type == MOUSEBUTTONUP:
            button_rectangle = pygame.rect.Rect(
                self.button_position.x,
                self.button_position.y,
                self.background_shadow_rectangle.w,
                self.background_shadow_rectangle.h,
            )

            if button_rectangle.collidepoint(event.pos):
                return True
        return False
