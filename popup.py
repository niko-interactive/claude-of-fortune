import pygame


class Popup:
    def __init__(self, message, font, screen_width, screen_height, phrase='', streak=None):
        self.font = font
        self.message = message
        self.phrase = phrase
        self.streak = streak

        self.rect = pygame.Rect(0, 0, 600, 250)
        self.rect.center = (screen_width // 2, screen_height // 2)

        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = self.rect.centerx
        self.button_rect.bottom = self.rect.bottom - 15

    def handle_click(self, pos):
        return self.button_rect.collidepoint(pos)

    def draw(self, screen):
        pygame.draw.rect(screen, 'black', self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 2)

        msg_surface = self.font.render(self.message, True, 'white')
        msg_rect = msg_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 30)
        screen.blit(msg_surface, msg_rect)

        phrase_surface = self.font.render(self.phrase, True, 'grey')
        phrase_rect = phrase_surface.get_rect(centerx=self.rect.centerx, top=msg_rect.bottom + 10)
        screen.blit(phrase_surface, phrase_rect)

        if self.streak is not None:
            streak_surface = self.font.render(f'Streak: {self.streak}', True, 'white')
            streak_rect = streak_surface.get_rect(centerx=self.rect.centerx, top=phrase_rect.bottom + 10)
            screen.blit(streak_surface, streak_rect)

        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_surface = self.font.render('Play Again', True, 'white')
        btn_rect = btn_surface.get_rect(center=self.button_rect.center)
        screen.blit(btn_surface, btn_rect)