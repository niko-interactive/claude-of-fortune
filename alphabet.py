import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP


class Alphabet:
    """
    Displays the full A-Z alphabet at the bottom of the screen.
    Letters darken when guessed to show the player what has already been tried.
    """

    def __init__(self, font, screen_width, screen_height):
        self.font = font

        # Tracks which letters have been guessed this round
        self.guessed = set()

        # Center the full row of letters horizontally at the bottom of the screen
        total_width = 26 * LETTER_SLOT_WIDTH + 25 * GAP
        start_x = (screen_width - total_width) // 2
        y = screen_height - LETTER_SLOT_HEIGHT - 20

        # Build a rect for each letter to use as a position reference when drawing
        self.letter_slots = {}
        for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            x = start_x + i * (LETTER_SLOT_WIDTH + GAP)
            self.letter_slots[char] = pygame.Rect(x, y, LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT)

    def guess(self, letter):
        """Mark a letter as guessed. Accepts upper or lowercase."""
        self.guessed.add(letter.upper())

    def draw(self, screen):
        """
        Draw all 26 letters. Guessed letters render in dark grey to fade
        into the background, unguessed letters render in white.
        """
        for char, rect in self.letter_slots.items():
            if char in self.guessed:
                surface = self.font.render(char, True, '#333333')
            else:
                surface = self.font.render(char, True, 'white')
            letter_rect = surface.get_rect(center=rect.center)
            screen.blit(surface, letter_rect)