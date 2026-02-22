import pygame


class Streak:
    """
    Draws the streak counter and coin balance in the top left corner.
    State (count, money) is owned by GameManager — this class only handles display.
    """

    def __init__(self, font):
        self.font = font

    def draw(self, screen, streak_count, money):
        """Draw the streak counter and coin balance."""
        streak_surface = self.font.render(f'STREAK  {streak_count}', True, 'white')
        screen.blit(streak_surface, (20, 20))

        money_surface = self.font.render(f'${money}', True, 'white')
        screen.blit(money_surface, (20, 60))