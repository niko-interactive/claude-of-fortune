import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP


class Strikes:
    """
    Tracks and displays the player's strikes for the current round.
    Shows a row of X marks in the top right corner:
      - Green X's on the left for bonus strikes (extra lives from consumables)
      - White X's for remaining regular strikes
      - Red X's for used regular strikes

    Max strikes can increase via upgrades. Bonus strike count is passed in
    at draw time and owned by GameManager.
    """

    def __init__(self, font, screen_width, max_strikes=3):
        self.font = font
        self.screen_width = screen_width
        self.max_strikes = max_strikes
        self.count = 0

    def _build_slots(self, num_slots):
        """Build a list of rects for num_slots X marks, flush to the top right."""
        total_width = num_slots * LETTER_SLOT_WIDTH + (num_slots - 1) * GAP
        start_x = self.screen_width - total_width - 20
        y = 20
        return [
            pygame.Rect(start_x + i * (LETTER_SLOT_WIDTH + GAP), y, LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT)
            for i in range(num_slots)
        ]

    def add_strike(self):
        """Add one strike after a wrong guess."""
        self.count += 1

    def is_game_over(self):
        """Return True if the player has used all their strikes."""
        return self.count >= self.max_strikes

    def draw(self, screen, bonus_strikes=0):
        """
        Draw all X marks. Bonus strikes appear as green X's on the left,
        followed by the regular strike slots (red for used, white for remaining).
        The total row width expands to accommodate bonus strikes.
        """
        total_slots = bonus_strikes + self.max_strikes
        slots = self._build_slots(total_slots)

        for i, rect in enumerate(slots):
            if i < bonus_strikes:
                color = 'green'
            elif i - bonus_strikes < self.count:
                color = 'red'
            else:
                color = 'white'
            surface = self.font.render('X', True, color)
            screen.blit(surface, surface.get_rect(center=rect.center))