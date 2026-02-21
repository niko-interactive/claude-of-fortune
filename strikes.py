import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP


class Strikes:
    def __init__(self, font, screen_width, max_strikes=3):
        self.font = font
        self.max_strikes = max_strikes
        self.count = 0

        total_width = max_strikes * LETTER_SLOT_WIDTH + (max_strikes - 1) * GAP
        start_x = screen_width - total_width - 20
        y = 20

        self.letter_slots = []
        for i in range(max_strikes):
            x = start_x + i * (LETTER_SLOT_WIDTH + GAP)
            self.letter_slots.append(pygame.Rect(x, y, LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT))

    def add_strike(self):
        self.count += 1

    def is_game_over(self):
        return self.count >= self.max_strikes

    def draw(self, screen):
        for i, rect in enumerate(self.letter_slots):
            color = 'red' if i < self.count else 'white'
            surface = self.font.render('X', True, color)
            x_rect = surface.get_rect(center=rect.center)
            screen.blit(surface, x_rect)
