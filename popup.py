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
        self.message = message
        self.phrase = phrase
        self.streak = streak
        self.game_complete = game_complete

        popup_width = 600
        padding = 40
        self.max_text_width = popup_width - padding * 2

        # Pre-wrap the phrase into lines that fit the popup width
        self.phrase_lines = self._wrap_text(phrase, self.font, self.max_text_width)

        # Calculate height dynamically based on content
        phrase_height = len(self.phrase_lines) * (self.font.get_height() + 4)
        streak_height = (self.font.get_height() + 10) if streak is not None else 0
        content_height = 30 + self.font.get_height() + 10 + phrase_height + streak_height + 20
        total_height = max(250, content_height + 63)  # 63 = button height + margins

        self.rect = pygame.Rect(0, 0, popup_width, total_height)
        self.rect.center = (screen_width // 2, screen_height // 2)

        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = self.rect.centerx
        self.button_rect.bottom = self.rect.bottom - 15

    def _wrap_text(self, text, font, max_width):
        """Split text into lines that fit within max_width pixels."""
        if not text:
            return []
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

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
            # Secret phrase shown in grey below the message, wrapped to fit
            y = next_top
            for line in self.phrase_lines:
                line_surface = self.font.render(line, True, 'grey')
                line_rect = line_surface.get_rect(centerx=self.rect.centerx, top=y)
                screen.blit(line_surface, line_rect)
                y += self.font.get_height() + 4

            # Final streak count
            if self.streak is not None:
                streak_surface = self.font.render(f'Streak: {self.streak}', True, 'white')
                streak_rect = streak_surface.get_rect(centerx=self.rect.centerx, top=y + 6)
                screen.blit(streak_surface, streak_rect)

        # Play Again button
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_label = 'New Game' if self.game_complete else 'Play Again'
        btn_surface = self.font.render(btn_label, True, 'white')
        btn_rect = btn_surface.get_rect(center=self.button_rect.center)
        screen.blit(btn_surface, btn_rect)