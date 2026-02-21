import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP


class Alphabet:
    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.guessed = set()

        total_width = 26 * LETTER_SLOT_WIDTH + 25 * GAP
        start_x = (screen_width - total_width) // 2
        y = screen_height - LETTER_SLOT_HEIGHT - 20

        self.letter_slots = {}
        for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            x = start_x + i * (LETTER_SLOT_WIDTH + GAP)
            self.letter_slots[char] = pygame.Rect(x, y, LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT)

    def guess(self, letter):
        self.guessed.add(letter.upper())

    def draw(self, screen):
        for char, rect in self.letter_slots.items():
            if char in self.guessed:
                surface = self.font.render(char, True, '#333333')
            else:
                surface = self.font.render(char, True, 'white')
            letter_rect = surface.get_rect(center=rect.center)
            screen.blit(surface, letter_rect)
