import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP


class Strikes:
    """
    Tracks and displays the player's strikes for the current round.
    Shows a row of X marks in the top right corner — white for remaining
    strikes and red for used ones. Max strikes can increase via upgrades.
    """

    def __init__(self, font, screen_width, max_strikes=3):
        self.font = font
        self.max_strikes = max_strikes  # 3 by default, can be 4 or 5 with upgrades
        self.count = 0                  # Number of strikes used so far this round

        # Position the row of X marks flush to the top right of the screen
        total_width = max_strikes * LETTER_SLOT_WIDTH + (max_strikes - 1) * GAP
        start_x = screen_width - total_width - 20
        y = 20

        # Build a rect for each strike position to use as a drawing reference
        self.letter_slots = []
        for i in range(max_strikes):
            x = start_x + i * (LETTER_SLOT_WIDTH + GAP)
            self.letter_slots.append(pygame.Rect(x, y, LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT))

    def add_strike(self):
        """Add one strike after a wrong guess."""
        self.count += 1

    def is_game_over(self):
        """Return True if the player has used all their strikes."""
        return self.count >= self.max_strikes

    def draw(self, screen):
        """
        Draw one X per strike slot. Used strikes render in red,
        remaining strikes render in white.
        """
        for i, rect in enumerate(self.letter_slots):
            color = 'red' if i < self.count else 'white'
            surface = self.font.render('X', True, color)
            x_rect = surface.get_rect(center=rect.center)
            screen.blit(surface, x_rect)