import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT


class Letter:
    def __init__(self, x, y, font, width=LETTER_SLOT_WIDTH, height=LETTER_SLOT_HEIGHT):
        self.rect = pygame.Rect(x, y, width, height)
        self.letter = None
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, 'white', self.rect, 2)
        if self.letter:
            surface = self.font.render(self.letter, True, 'white')
            letter_rect = surface.get_rect(center=self.rect.center)
            screen.blit(surface, letter_rect)
