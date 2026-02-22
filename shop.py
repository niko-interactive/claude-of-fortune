import pygame
import random


# --- Upgrade Definitions ---
# Upgrades are permanent until the player loses.
# Prerequisites must be purchased before the next tier becomes visible.
UPGRADES = [
    {
        'id': 'auto_consonant',
        'label': 'Free Consonant',
        'description': 'A random consonant is revealed each round',
        'cost': 50,
        'requires': None,
    },
    {
        'id': 'auto_consonant_guaranteed',
        'label': 'Guaranteed Consonant',
        'description': 'Free consonant is guaranteed to be in the phrase',
        'cost': 100,
        'requires': 'auto_consonant',
    },    
    {
        'id': 'auto_vowel',
        'label': 'Free Vowel',
        'description': 'A random vowel is revealed each round',
        'cost': 100,
        'requires': None,
    },
    {
        'id': 'auto_vowel_guaranteed',
        'label': 'Guaranteed Vowel',
        'description': 'Free vowel is guaranteed to be in the phrase',
        'cost': 200,
        'requires': 'auto_vowel',
    },
    {
        'id': 'extra_strike_1',
        'label': '4th Strike',
        'description': 'Gain a 4th strike before losing',
        'cost': 250,
        'requires': None,
    },
    {
        'id': 'extra_strike_2',
        'label': '5th Strike',
        'description': 'Gain a 5th strike before losing',
        'cost': 500,
        'requires': 'extra_strike_1',
    },

]

# --- Consumable Definitions ---
# Consumables are single use and applied immediately upon purchase mid-round.
CONSUMABLES = [
    {
        'id': 'reveal_consonant',
        'label': 'Reveal Consonant',
        'description': 'Reveals a random hidden consonant in the phrase',
        'cost': 25,
    },
    {
        'id': 'reveal_vowel',
        'label': 'Reveal Vowel',
        'description': 'Reveals a random hidden vowel in the phrase',
        'cost': 50,
    },
    {
        'id': 'eliminate_letters',
        'label': 'Eliminate 3 Letters',
        'description': 'Removes 3 wrong letters from the alphabet',
        'cost': 25,
    },
    {
        'id': 'free_guess',
        'label': 'Free Guess',
        'description': 'Next wrong guess does not cost a strike',
        'cost': 50,
    },
]

VOWELS = set('AEIOU')
CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')

ROW_HEIGHT = 52      # Height of each item row
BTN_WIDTH = 80
BTN_HEIGHT = 36


class Shop:
    """
    Manages the shop system including upgrades and consumables.
    Upgrades are permanent until the player loses.
    Consumables are purchased and used immediately.
    Money is earned based on puzzle difficulty and resets on loss.
    Upgrades with prerequisites are hidden until the prereq is purchased.
    """

    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.money = 0
        self.purchased_upgrades = set()  # ids of permanently owned upgrades
        self.free_guess_active = False   # True if a free guess consumable is active
        self.visible = False
        self.active_tab = 'upgrades'     # 'upgrades' or 'consumables'

        # Callbacks set by main.py to allow consumables to affect game state
        self.on_reveal_consonant = None
        self.on_reveal_vowel = None
        self.on_eliminate_letters = None

        # Shop button centered at the top of the screen
        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = screen_width // 2
        self.button_rect.top = 20

        # Popup centered on screen — width set to 600
        self.popup_rect = pygame.Rect(0, 0, 600, 480)
        self.popup_rect.center = (screen_width // 2, screen_height // 2)

        # Two tabs, centered horizontally in the popup
        tab_width = 220
        tab_height = 36
        total_tabs_width = tab_width * 2 + 20  # 20px gap between tabs
        tab_start_x = self.popup_rect.left + (self.popup_rect.width - total_tabs_width) // 2
        tab_y = self.popup_rect.top + 55
        self.tab_upgrades_rect = pygame.Rect(tab_start_x, tab_y, tab_width, tab_height)
        self.tab_consumables_rect = pygame.Rect(tab_start_x + tab_width + 20, tab_y, tab_width, tab_height)

        # Close button centered at the bottom of the popup
        self.close_rect = pygame.Rect(0, 0, 120, 40)
        self.close_rect.centerx = self.popup_rect.centerx
        self.close_rect.bottom = self.popup_rect.bottom - 15

        # Buy button rects for consumables (fixed positions)
        self.consumable_buy_rects = {}
        for i, consumable in enumerate(CONSUMABLES):
            y = self.popup_rect.top + 110 + i * ROW_HEIGHT
            rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
            rect.right = self.popup_rect.right - 20
            rect.centery = y + ROW_HEIGHT // 2
            self.consumable_buy_rects[consumable['id']] = rect

    def _visible_upgrades(self):
        """
        Return only upgrades that should currently be visible.
        Upgrades with a prereq are hidden until the prereq is purchased.
        """
        return [u for u in UPGRADES
                if u['requires'] is None or u['requires'] in self.purchased_upgrades]

    def earn(self, difficulty, strikes_left, streak):
        """Award coins based on puzzle difficulty and strikes remaining.
        Formula: difficulty / 10 * max(streak / 10, 1) * (1 + 0.05 * strikes_left), rounded to nearest integer."""
        self.money += round(difficulty / 10 * max(streak / 10, 1) * (1 + 0.05 * strikes_left))

    def reset(self):
        """Reset all shop state on a loss."""
        self.money = 0
        self.purchased_upgrades = set()
        self.free_guess_active = False

    def is_upgrade_available(self, upgrade):
        """Return True if the upgrade can be purchased — not already owned and prereq met."""
        if upgrade['id'] in self.purchased_upgrades:
            return False
        if upgrade['requires'] and upgrade['requires'] not in self.purchased_upgrades:
            return False
        return True

    def max_strikes(self):
        """Return total strikes based on purchased strike upgrades."""
        strikes = 3
        if 'extra_strike_1' in self.purchased_upgrades:
            strikes += 1
        if 'extra_strike_2' in self.purchased_upgrades:
            strikes += 1
        return strikes

    def get_auto_guesses(self, phrase_word):
        """
        Return letters to auto-reveal at the start of a round based on
        purchased upgrades. Guaranteed upgrades pull from letters in the phrase,
        random upgrades pull from the full alphabet pool.
        """
        guesses = []
        phrase_letters = set(c for c in phrase_word if c.isalpha())

        if 'auto_consonant' in self.purchased_upgrades:
            guaranteed = 'auto_consonant_guaranteed' in self.purchased_upgrades
            pool = list(phrase_letters & CONSONANTS) if guaranteed else list(CONSONANTS)
            if not pool:
                pool = list(CONSONANTS)
            guesses.append(random.choice(pool))

        if 'auto_vowel' in self.purchased_upgrades:
            guaranteed = 'auto_vowel_guaranteed' in self.purchased_upgrades
            pool = list(phrase_letters & VOWELS) if guaranteed else list(VOWELS)
            if not pool:
                pool = list(VOWELS)
            guesses.append(random.choice(pool))

        return guesses

    def use_free_guess(self):
        """
        Check if a free guess is active and consume it.
        Returns True if the strike should be blocked.
        """
        if self.free_guess_active:
            self.free_guess_active = False
            return True
        return False

    def _try_purchase_upgrade(self, upgrade_id):
        """Attempt to purchase an upgrade. Returns True if successful."""
        upgrade = next((u for u in UPGRADES if u['id'] == upgrade_id), None)
        if not upgrade or not self.is_upgrade_available(upgrade):
            return False
        if self.money < upgrade['cost']:
            return False
        self.money -= upgrade['cost']
        self.purchased_upgrades.add(upgrade_id)
        return True

    def _try_purchase_consumable(self, consumable_id):
        """Attempt to purchase and immediately use a consumable."""
        consumable = next((c for c in CONSUMABLES if c['id'] == consumable_id), None)
        if not consumable or self.money < consumable['cost']:
            return False
        self.money -= consumable['cost']

        if consumable_id == 'reveal_consonant' and self.on_reveal_consonant:
            self.on_reveal_consonant()
        elif consumable_id == 'reveal_vowel' and self.on_reveal_vowel:
            self.on_reveal_vowel()
        elif consumable_id == 'eliminate_letters' and self.on_eliminate_letters:
            self.on_eliminate_letters()
        elif consumable_id == 'free_guess':
            self.free_guess_active = True

        return True

    def handle_click(self, pos):
        """Handle all clicks for the shop button, tabs, buy buttons, and close."""
        if self.button_rect.collidepoint(pos):
            self.visible = not self.visible
            return True

        if not self.visible:
            return False

        if self.close_rect.collidepoint(pos):
            self.visible = False
            return True

        if self.tab_upgrades_rect.collidepoint(pos):
            self.active_tab = 'upgrades'
            return True

        if self.tab_consumables_rect.collidepoint(pos):
            self.active_tab = 'consumables'
            return True

        if self.active_tab == 'upgrades':
            # Build click rects dynamically to match visible rows
            visible = self._visible_upgrades()
            for i, upgrade in enumerate(visible):
                y = self.popup_rect.top + 110 + i * ROW_HEIGHT
                rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
                rect.right = self.popup_rect.right - 20
                rect.centery = y + ROW_HEIGHT // 2
                if rect.collidepoint(pos):
                    self._try_purchase_upgrade(upgrade['id'])
                    return True

        if self.active_tab == 'consumables':
            for consumable_id, rect in self.consumable_buy_rects.items():
                if rect.collidepoint(pos):
                    self._try_purchase_consumable(consumable_id)
                    return True

        return False

    def _draw_tab_content(self, screen):
        """Draw the rows for whichever tab is active."""
        if self.active_tab == 'upgrades':
            visible = self._visible_upgrades()

            for i, upgrade in enumerate(visible):
                y = self.popup_rect.top + 110 + i * ROW_HEIGHT
                owned = upgrade['id'] in self.purchased_upgrades
                can_afford = self.money >= upgrade['cost']

                # Label always white (dimmed if owned), description always grey
                label_color = '#555555' if owned else 'white'
                label_surf = self.small_font.render(upgrade['label'], True, label_color)
                desc_surf = self.small_font.render(upgrade['description'], True, '#888888')
                screen.blit(label_surf, (self.popup_rect.left + 20, y + 6))
                screen.blit(desc_surf, (self.popup_rect.left + 20, y + 26))

                # Buy button vertically centered in the row
                rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
                rect.right = self.popup_rect.right - 20
                rect.centery = y + ROW_HEIGHT // 2

                if owned:
                    btn_color, btn_text, text_color, border_color = '#333333', 'Owned', '#555555', '#555555'
                elif not can_afford:
                    btn_color, btn_text, text_color, border_color = '#222222', f'${upgrade["cost"]}', '#555555', '#555555'
                else:
                    btn_color, btn_text, text_color, border_color = 'black', f'${upgrade["cost"]}', 'white', 'white'

                pygame.draw.rect(screen, btn_color, rect)
                pygame.draw.rect(screen, border_color, rect, 1)
                btn_surf = self.small_font.render(btn_text, True, text_color)
                screen.blit(btn_surf, btn_surf.get_rect(center=rect.center))

        else:  # consumables tab
            for i, consumable in enumerate(CONSUMABLES):
                y = self.popup_rect.top + 110 + i * ROW_HEIGHT
                can_afford = self.money >= consumable['cost']

                # Label always white, description always grey
                label_surf = self.small_font.render(consumable['label'], True, 'white')
                desc_surf = self.small_font.render(consumable['description'], True, '#888888')
                screen.blit(label_surf, (self.popup_rect.left + 20, y + 6))
                screen.blit(desc_surf, (self.popup_rect.left + 20, y + 26))

                # Buy button vertically centered in the row — rebuilt each
                # frame so click detection always matches draw position
                rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
                rect.right = self.popup_rect.right - 20
                rect.centery = y + ROW_HEIGHT // 2
                self.consumable_buy_rects[consumable['id']] = rect
                btn_color = 'black' if can_afford else '#222222'
                text_color = 'white' if can_afford else '#555555'
                border_color = 'white' if can_afford else '#555555'

                pygame.draw.rect(screen, btn_color, rect)
                pygame.draw.rect(screen, border_color, rect, 1)
                btn_surf = self.small_font.render(f'${consumable["cost"]}', True, text_color)
                screen.blit(btn_surf, btn_surf.get_rect(center=rect.center))

    def draw(self, screen):
        """Draw the shop button and popup if visible."""
        # Shop button
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_surface = self.font.render('Shop', True, 'white')
        screen.blit(btn_surface, btn_surface.get_rect(center=self.button_rect.center))

        if not self.visible:
            return

        # Popup background and border
        pygame.draw.rect(screen, 'black', self.popup_rect)
        pygame.draw.rect(screen, 'white', self.popup_rect, 2)

        # Title centered at the top
        title = self.font.render('SHOP', True, 'white')
        screen.blit(title, title.get_rect(centerx=self.popup_rect.centerx, top=self.popup_rect.top + 15))

        # Tabs centered horizontally
        for tab_id, rect, label in [
            ('upgrades', self.tab_upgrades_rect, 'Upgrades'),
            ('consumables', self.tab_consumables_rect, 'Consumables'),
        ]:
            is_active = self.active_tab == tab_id
            pygame.draw.rect(screen, '#222222' if is_active else 'black', rect)
            pygame.draw.rect(screen, 'white', rect, 2 if is_active else 1)
            tab_surf = self.small_font.render(label, True, 'white')
            screen.blit(tab_surf, tab_surf.get_rect(center=rect.center))

        # Divider below tabs
        pygame.draw.line(screen, 'grey',
                         (self.popup_rect.left + 20, self.popup_rect.top + 100),
                         (self.popup_rect.right - 20, self.popup_rect.top + 100), 1)

        self._draw_tab_content(screen)

        # Free guess indicator at the bottom of the popup when active
        if self.free_guess_active:
            fg_surf = self.small_font.render('FREE GUESS ACTIVE', True, 'green')
            screen.blit(fg_surf, (self.popup_rect.left + 20, self.popup_rect.bottom - 55))

        # Close button
        pygame.draw.rect(screen, 'black', self.close_rect)
        pygame.draw.rect(screen, 'white', self.close_rect, 2)
        close_surf = self.font.render('Close', True, 'white')
        screen.blit(close_surf, close_surf.get_rect(center=self.close_rect.center))