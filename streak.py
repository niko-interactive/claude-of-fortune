import pygame


class Streak:
    def __init__(self, font):
        self.font = font
        self.count = 0
        self.previous = 0

    def win(self):
        self.count += 1

    def lose(self):
        self.previous = self.count
        self.count = 0

    def draw(self, screen):
        surface = self.font.render(f'STREAK  {self.count}', True, 'white')
        screen.blit(surface, (20, 20))