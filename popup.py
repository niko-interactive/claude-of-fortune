import pygame


class Popup:
    """
    Modal overlay shown at the end of a round.
    Displays a win or lose message, the secret phrase, and optionally
    the player's final streak if they lost. Contains a Play Again button
    to start the next round.

    game_complete=True is used for the special "You Beat the Game!" screen
    shown when the player clears every puzzle in a run. It omits the phrase
    and streak, and the Play Again button resets everything from scratch.
    """

    def __init__(self, message, font, screen_width, screen_height,
                 phrase='', streak=None, game_complete=False):
        self.font = font
        self.small_font = pygame.font.SysFont('Arial', 22)
        self.message = message      # 'You Win!', 'You Lose!', or 'You Beat the Game!'
        self.phrase = phrase        # The secret phrase revealed at round end
        self.streak = streak        # Final streak count, only passed on a loss
        self.game_complete = game_complete  # True for the all-puzzles-cleared screen

        # Center the popup box on screen — taller for game_complete
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

        # Win/lose/complete message
        msg_color = 'gold' if self.game_complete else 'white'
        msg_surface = self.font.render(self.message, True, msg_color)
        msg_rect = msg_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        screen.blit(msg_surface, msg_rect)

        next_top = msg_rect.bottom + 10

        if self.game_complete:
            # Congratulatory subtext
            sub_surface = self.small_font.render("You've solved every puzzle. Consider going outside...", True, 'green')
            sub_rect = sub_surface.get_rect(centerx=self.rect.centerx, top=next_top)
            screen.blit(sub_surface, sub_rect)

            if self.streak is not None:
                streak_surface = self.font.render(f'Streak: {self.streak}', True, 'white')
                streak_rect = streak_surface.get_rect(centerx=self.rect.centerx,
                                                      top=next_top + 40)
                screen.blit(streak_surface, streak_rect)

        else:
            # Secret phrase shown in grey below the message
            phrase_surface = self.font.render(self.phrase, True, 'grey')
            phrase_rect = phrase_surface.get_rect(centerx=self.rect.centerx, top=next_top)
            screen.blit(phrase_surface, phrase_rect)

            # Final streak count
            if self.streak is not None:
                streak_surface = self.font.render(f'Streak: {self.streak}', True, 'white')
                streak_rect = streak_surface.get_rect(centerx=self.rect.centerx,
                                                      top=phrase_rect.bottom + 10)
                screen.blit(streak_surface, streak_rect)

        # Play Again button
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_label = 'New Game' if self.game_complete else 'Play Again'
        btn_surface = self.font.render(btn_label, True, 'white')
        btn_rect = btn_surface.get_rect(center=self.button_rect.center)
        screen.blit(btn_surface, btn_rect)