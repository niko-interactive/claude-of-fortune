import pygame
import random


# Each upgrade has a unique id, a display label, and the streak required to unlock it.
# Upgrades are checked in order — later upgrades build on earlier ones where applicable.
UPGRADES = [
    {
        'id': 'auto_consonant',
        'label': 'Free Consonant (Random)',
        'streak_required': 3,
    },
    {
        'id': 'auto_consonant_guaranteed',
        'label': 'Free Consonant (Guaranteed)',
        'streak_required': 5,
    },
    {
        'id': 'extra_strike_1',
        'label': '4th Strike',
        'streak_required': 7,
    },
    {
        'id': 'auto_vowel',
        'label': 'Free Vowel (Random)',
        'streak_required': 9,
    },
    {
        'id': 'auto_vowel_guaranteed',
        'label': 'Free Vowel (Guaranteed)',
        'streak_required': 11,
    },
    {
        'id': 'extra_strike_2',
        'label': '5th Strike',
        'streak_required': 13,
    },
]

VOWELS = set('AEIOU')
CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')


class Upgrades:
    """
    Manages the passive upgrade system. Upgrades unlock automatically
    when the player reaches the required streak and apply at the start
    of each round without any player interaction.

    Also handles the upgrades button and popup menu where players can
    see what they have unlocked and what is still locked.
    """

    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False  # Whether the upgrades popup is currently open

        # Upgrades button centered at the top of the screen
        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = screen_width // 2
        self.button_rect.top = 20

        # Popup menu centered on screen
        self.popup_rect = pygame.Rect(0, 0, 420, 420)
        self.popup_rect.center = (screen_width // 2, screen_height // 2)

        # Close button at the bottom of the popup
        self.close_rect = pygame.Rect(0, 0, 120, 40)
        self.close_rect.centerx = self.popup_rect.centerx
        self.close_rect.bottom = self.popup_rect.bottom - 15

    def get_unlocked(self, streak_count):
        """Return a set of upgrade ids that are unlocked at the given streak count."""
        return {u['id'] for u in UPGRADES if streak_count >= u['streak_required']}

    def max_strikes(self, streak_count):
        """
        Return the total number of strikes available based on unlocked upgrades.
        Starts at 3, increases to 4 at streak 7 and 5 at streak 13.
        """
        unlocked = self.get_unlocked(streak_count)
        strikes = 3
        if 'extra_strike_1' in unlocked:
            strikes += 1
        if 'extra_strike_2' in unlocked:
            strikes += 1
        return strikes

    def get_auto_guesses(self, phrase_word, streak_count):
        """
        Return a list of letters to automatically guess at the start of a round.
        These are applied silently and never cost a strike.

        Consonant and vowel guesses each have two tiers:
        - Random: picks from the full alphabet pool
        - Guaranteed: picks only from letters that actually appear in the phrase,
          falling back to the full pool if no matching letters exist
        """
        unlocked = self.get_unlocked(streak_count)
        guesses = []
        phrase_letters = set(c for c in phrase_word if c.isalpha())

        if 'auto_consonant' in unlocked:
            guaranteed = 'auto_consonant_guaranteed' in unlocked
            if guaranteed:
                # Only pick consonants that are actually in the phrase
                pool = list(phrase_letters & CONSONANTS)
                if not pool:
                    pool = list(CONSONANTS)  # Fallback if phrase has no consonants
            else:
                pool = list(CONSONANTS)  # Purely random from full consonant set
            guesses.append(random.choice(pool))

        if 'auto_vowel' in unlocked:
            guaranteed = 'auto_vowel_guaranteed' in unlocked
            if guaranteed:
                # Only pick vowels that are actually in the phrase
                pool = list(phrase_letters & VOWELS)
                if not pool:
                    pool = list(VOWELS)  # Fallback if phrase has no vowels
            else:
                pool = list(VOWELS)  # Purely random from full vowel set
            guesses.append(random.choice(pool))

        return guesses

    def handle_click(self, pos, streak_count):
        """
        Handle mouse clicks for the upgrades button and close button.
        Returns True if a click was handled, False otherwise.
        """
        if self.button_rect.collidepoint(pos):
            self.visible = not self.visible  # Toggle the popup open/closed
            return True
        if self.visible and self.close_rect.collidepoint(pos):
            self.visible = False
            return True
        return False

    def draw(self, screen, streak_count):
        """
        Draw the upgrades button. If the popup is open, also draw the full
        upgrades table with streak requirements and unlock status.
        """
        # Always draw the button
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_surface = self.font.render('Upgrades', True, 'white')
        btn_rect = btn_surface.get_rect(center=self.button_rect.center)
        screen.blit(btn_surface, btn_rect)

        if not self.visible:
            return

        # Popup background and border
        pygame.draw.rect(screen, 'black', self.popup_rect)
        pygame.draw.rect(screen, 'white', self.popup_rect, 2)

        # Title
        title = self.font.render('UPGRADES', True, 'white')
        title_rect = title.get_rect(centerx=self.popup_rect.centerx, top=self.popup_rect.top + 20)
        screen.blit(title, title_rect)

        # Column headers
        small_font = pygame.font.SysFont('Arial', 22)
        col_x_streak = self.popup_rect.left + 40
        col_x_label = self.popup_rect.left + 120

        headers = [('Streak', col_x_streak), ('Upgrade', col_x_label)]
        for text, x in headers:
            surf = small_font.render(text, True, 'grey')
            screen.blit(surf, (x, self.popup_rect.top + 65))

        # Divider line under headers
        pygame.draw.line(screen, 'grey',
                         (self.popup_rect.left + 20, self.popup_rect.top + 85),
                         (self.popup_rect.right - 20, self.popup_rect.top + 85), 1)

        # Draw each upgrade row — white if unlocked, dark grey if still locked
        unlocked = self.get_unlocked(streak_count)
        for i, upgrade in enumerate(UPGRADES):
            y = self.popup_rect.top + 100 + i * 45
            is_unlocked = upgrade['id'] in unlocked
            color = 'white' if is_unlocked else '#555555'

            streak_surf = small_font.render(str(upgrade['streak_required']), True, color)
            label_surf = small_font.render(upgrade['label'], True, color)

            screen.blit(streak_surf, (col_x_streak, y))
            screen.blit(label_surf, (col_x_label, y))

        # Close button
        pygame.draw.rect(screen, 'black', self.close_rect)
        pygame.draw.rect(screen, 'white', self.close_rect, 2)
        close_surf = self.font.render('Close', True, 'white')
        close_text_rect = close_surf.get_rect(center=self.close_rect.center)
        screen.blit(close_surf, close_text_rect)