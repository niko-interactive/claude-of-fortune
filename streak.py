import pygame


class Streak:
    """
    Tracks the player's current win streak across rounds.
    Persists between rounds and is never reset by reset_game —
    only a loss resets the count.
    """

    def __init__(self, font):
        self.font = font
        self.count = 0     # Current active streak
        self.previous = 0  # Streak count before the last loss, used in the lose popup

    def win(self):
        """Increment the streak by one after a win."""
        self.count += 1

    def lose(self):
        """Save the current streak then reset it to zero after a loss."""
        self.previous = self.count
        self.count = 0

    def draw(self, screen):
        """Draw the streak counter in the top left corner of the screen."""
        surface = self.font.render(f'STREAK  {self.count}', True, 'white')
        screen.blit(surface, (20, 20))