import pygame


class Popup:
    """
    Modal overlay shown at the end of a round.
    Displays a win or lose message, the secret phrase, and optionally
    the player's final streak if they lost. Contains a Play Again button
    to start the next round.
    """

    def __init__(self, message, font, screen_width, screen_height, phrase='', streak=None):
        self.font = font
        self.message = message  # 'You Win!' or 'You Lose!'
        self.phrase = phrase    # The secret phrase revealed at round end
        self.streak = streak    # Final streak count, only passed on a loss

        # Center the popup box on screen
        self.rect = pygame.Rect(0, 0, 600, 250)
        self.rect.center = (screen_width // 2, screen_height // 2)

        # Play Again button positioned at the bottom of the popup
        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = self.rect.centerx
        self.button_rect.bottom = self.rect.bottom - 15

    def handle_click(self, pos):
        """Return True if the Play Again button was clicked."""
        return self.button_rect.collidepoint(pos)

    def draw(self, screen):
        """
        Draw the popup box, win/lose message, secret phrase, optional
        streak count, and the Play Again button.
        """
        # Background and border
        pygame.draw.rect(screen, 'black', self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 2)

        # Win or lose message
        msg_surface = self.font.render(self.message, True, 'white')
        msg_rect = msg_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        screen.blit(msg_surface, msg_rect)

        # Secret phrase shown in grey below the message
        phrase_surface = self.font.render(self.phrase, True, 'grey')
        phrase_rect = phrase_surface.get_rect(centerx=self.rect.centerx, top=msg_rect.bottom + 10)
        screen.blit(phrase_surface, phrase_rect)

        # Final streak count — only shown on a loss
        if self.streak is not None:
            streak_surface = self.font.render(f'Streak: {self.streak}', True, 'white')
            streak_rect = streak_surface.get_rect(centerx=self.rect.centerx, top=phrase_rect.bottom + 10)
            screen.blit(streak_surface, streak_rect)

        # Play Again button
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_surface = self.font.render('Play Again', True, 'white')
        btn_rect = btn_surface.get_rect(center=self.button_rect.center)
        screen.blit(btn_surface, btn_rect)