import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT


class Letter:
    """
    Represents a single letter slot in the phrase.
    Draws as an empty white outlined box until a matching letter is guessed,
    at which point the letter is revealed inside the box.
    """

    def __init__(self, x, y, font, width=LETTER_SLOT_WIDTH, height=LETTER_SLOT_HEIGHT):
        # Position and size of the slot on screen
        self.rect = pygame.Rect(x, y, width, height)

        # None means the letter is hidden, a string means it has been revealed
        self.letter = None

        self.font = font

    def draw(self, screen):
        """
        Draw the letter slot. Always draws the outline box.
        If the letter has been revealed, draws the character centered inside.
        """
        pygame.draw.rect(screen, 'white', self.rect, 2)
        if self.letter:
            surface = self.font.render(self.letter, True, 'white')
            letter_rect = surface.get_rect(center=self.rect.center)
            screen.blit(surface, letter_rect)