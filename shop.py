import pygame

from shop_items import UPGRADES, CONSUMABLES


ROW_HEIGHT = 52
BTN_WIDTH = 80
BTN_HEIGHT = 36


class Shop:
    """
    Manages the shop UI and purchase rules for upgrades and consumables.
    Upgrades are permanent until the player loses.
    Consumables are purchased and used immediately.

    Money and purchased_upgrades are owned by GameManager. The shop reads
    them via manager references and never tracks them itself. Consumable
    effects are registered as callbacks by GameManager each round.

    The content area of each tab scrolls independently. Adding a new tab
    means adding a key to self.scroll_offsets and a branch in the draw/click
    methods — the scroll infrastructure handles the rest automatically.
    """

    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.free_guess_active = False   # True if a free guess consumable is active
        self.visible = False
        self.active_tab = 'upgrades'     # 'upgrades' or 'consumables'

        # Per-tab scroll offsets in pixels — add a key here when adding a new tab
        self.scroll_offsets = {
            'upgrades': 0,
            'consumables': 0,
        }

        # Set by GameManager each round — called when a consumable is purchased
        self.on_reveal_consonant = None
        self.on_reveal_vowel = None
        self.on_eliminate_letters = None

        # Set by main.py after GameManager is created
        self.manager = None

        # Shop button centered at the top of the screen
        self.button_rect = pygame.Rect(0, 0, 160, 48)
        self.button_rect.centerx = screen_width // 2
        self.button_rect.top = 20

        # Popup centered on screen
        self.popup_rect = pygame.Rect(0, 0, 600, 480)
        self.popup_rect.center = (screen_width // 2, screen_height // 2)

        # Tabs centered horizontally in the popup — sized to fit two tabs with a gap.
        # To add a third tab, adjust tab_width and total_tabs_width accordingly.
        tab_width = 220
        tab_height = 36
        total_tabs_width = tab_width * 2 + 20
        tab_start_x = self.popup_rect.left + (self.popup_rect.width - total_tabs_width) // 2
        tab_y = self.popup_rect.top + 55
        self.tab_rects = {
            'upgrades':    pygame.Rect(tab_start_x,              tab_y, tab_width, tab_height),
            'consumables': pygame.Rect(tab_start_x + tab_width + 20, tab_y, tab_width, tab_height),
        }

        # Scrollable content area — sits below the tab row, above the close button.
        # Inset by 2px on each side to stay inside the popup border.
        self.content_top = self.popup_rect.top + 110
        self.content_bottom = self.popup_rect.bottom - 65  # leaves room for close button
        self.content_height = self.content_bottom - self.content_top
        self.content_rect = pygame.Rect(
            self.popup_rect.left + 2,
            self.content_top,
            self.popup_rect.width - 4,
            self.content_height,
        )

        # Close button centered at the bottom of the popup
        self.close_rect = pygame.Rect(0, 0, 120, 40)
        self.close_rect.centerx = self.popup_rect.centerx
        self.close_rect.bottom = self.popup_rect.bottom - 15

    # --- State ---

    def reset(self):
        """Reset consumable state on a loss. Upgrades are reset by GameManager."""
        self.free_guess_active = False

    def _visible_upgrades(self, purchased_upgrades):
        """Return upgrades that should be visible — prereq must be purchased first."""
        return [u for u in UPGRADES
                if u['requires'] is None or u['requires'] in purchased_upgrades]

    def is_upgrade_available(self, upgrade, purchased_upgrades):
        """Return True if the upgrade can be purchased — not already owned and prereq met."""
        if upgrade['id'] in purchased_upgrades:
            return False
        if upgrade['requires'] and upgrade['requires'] not in purchased_upgrades:
            return False
        return True

    def use_free_guess(self):
        """Consume a free guess if active. Returns True if a strike should be blocked."""
        if self.free_guess_active:
            self.free_guess_active = False
            return True
        return False

    # --- Purchases ---

    def _try_purchase_upgrade(self, upgrade_id):
        """Attempt to purchase an upgrade. Returns True if successful."""
        purchased = self.manager.purchased_upgrades
        upgrade = next((u for u in UPGRADES if u['id'] == upgrade_id), None)
        if not upgrade or not self.is_upgrade_available(upgrade, purchased):
            return False
        if not self.manager.spend(upgrade['cost']):
            return False
        purchased.add(upgrade_id)
        return True

    def _try_purchase_consumable(self, consumable_id):
        """Attempt to purchase and immediately apply a consumable."""
        consumable = next((c for c in CONSUMABLES if c['id'] == consumable_id), None)
        if not consumable:
            return False
        if not self.manager.spend(consumable['cost']):
            return False

        if consumable_id == 'reveal_consonant' and self.on_reveal_consonant:
            self.on_reveal_consonant()
        elif consumable_id == 'reveal_vowel' and self.on_reveal_vowel:
            self.on_reveal_vowel()
        elif consumable_id == 'eliminate_letters' and self.on_eliminate_letters:
            self.on_eliminate_letters()
        elif consumable_id == 'free_guess':
            self.free_guess_active = True

        return True

    # --- Scroll ---

    def _max_scroll(self, tab, purchased_upgrades):
        """Return the maximum scroll offset for a tab based on its total content height."""
        if tab == 'upgrades':
            count = len(self._visible_upgrades(purchased_upgrades))
        else:
            count = len(CONSUMABLES)
        total_content_height = count * ROW_HEIGHT
        return max(0, total_content_height - self.content_height)

    def scroll(self, dy, purchased_upgrades):
        """
        Scroll the active tab by dy pixels (negative = scroll down, positive = scroll up).
        Clamps to valid range so content never scrolls past its bounds.
        """
        if not self.visible:
            return
        max_scroll = self._max_scroll(self.active_tab, purchased_upgrades)
        current = self.scroll_offsets[self.active_tab]
        self.scroll_offsets[self.active_tab] = max(0, min(current - dy * 20, max_scroll))

    def _switch_tab(self, tab):
        """Switch to a tab. Scroll offset for each tab is preserved independently."""
        self.active_tab = tab

    # --- Click Handling ---

    def handle_click(self, pos, purchased_upgrades):
        """Handle all clicks for the shop button, tabs, buy buttons, and close."""
        if self.button_rect.collidepoint(pos):
            self.visible = not self.visible
            return True

        if not self.visible:
            return False

        if self.close_rect.collidepoint(pos):
            self.visible = False
            return True

        for tab_id, rect in self.tab_rects.items():
            if rect.collidepoint(pos):
                self._switch_tab(tab_id)
                return True

        # Only register clicks inside the scrollable content area
        if not self.content_rect.collidepoint(pos):
            return False

        scroll = self.scroll_offsets[self.active_tab]
        # Translate screen position into content-surface position
        content_y = pos[1] - self.content_top + scroll

        if self.active_tab == 'upgrades':
            visible = self._visible_upgrades(purchased_upgrades)
            for i, upgrade in enumerate(visible):
                row_y = i * ROW_HEIGHT
                btn_rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
                btn_rect.right = self.popup_rect.right - 20 - self.popup_rect.left
                btn_rect.centery = row_y + ROW_HEIGHT // 2
                if btn_rect.left <= pos[0] - self.popup_rect.left <= btn_rect.right:
                    if btn_rect.top <= content_y <= btn_rect.bottom:
                        self._try_purchase_upgrade(upgrade['id'])
                        return True

        elif self.active_tab == 'consumables':
            for i, consumable in enumerate(CONSUMABLES):
                row_y = i * ROW_HEIGHT
                btn_rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
                btn_rect.right = self.popup_rect.right - 20 - self.popup_rect.left
                btn_rect.centery = row_y + ROW_HEIGHT // 2
                if btn_rect.left <= pos[0] - self.popup_rect.left <= btn_rect.right:
                    if btn_rect.top <= content_y <= btn_rect.bottom:
                        self._try_purchase_consumable(consumable['id'])
                        return True

        return False

    # --- Drawing ---

    def _draw_tab_content(self, screen, money, purchased_upgrades):
        """
        Draw the scrollable content for the active tab.
        Renders all rows onto an offscreen surface, then blits a clipped
        window of it onto the popup at the correct scroll position.
        """
        if self.active_tab == 'upgrades':
            items = self._visible_upgrades(purchased_upgrades)
        else:
            items = CONSUMABLES

        total_height = max(len(items) * ROW_HEIGHT, self.content_height)
        content_surface = pygame.Surface((self.popup_rect.width, total_height))
        content_surface.fill('black')

        for i, item in enumerate(items):
            y = i * ROW_HEIGHT
            is_upgrade = self.active_tab == 'upgrades'

            if is_upgrade:
                owned = item['id'] in purchased_upgrades
                can_afford = money >= item['cost']
                label_color = '#555555' if owned else 'white'
            else:
                owned = False
                can_afford = money >= item['cost']
                label_color = 'white'

            label_surf = self.small_font.render(item['label'], True, label_color)
            desc_surf = self.small_font.render(item['description'], True, '#888888')
            content_surface.blit(label_surf, (20, y + 6))
            content_surface.blit(desc_surf, (20, y + 26))

            btn_rect = pygame.Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
            btn_rect.right = self.popup_rect.width - 20
            btn_rect.centery = y + ROW_HEIGHT // 2

            if owned:
                btn_color, btn_text, text_color, border_color = '#333333', 'Owned', '#555555', '#555555'
            elif not can_afford:
                btn_color, btn_text, text_color, border_color = '#222222', f'${item["cost"]}', '#555555', '#555555'
            else:
                btn_color, btn_text, text_color, border_color = 'black', f'${item["cost"]}', 'white', 'white'

            pygame.draw.rect(content_surface, btn_color, btn_rect)
            pygame.draw.rect(content_surface, border_color, btn_rect, 1)
            btn_surf = self.small_font.render(btn_text, True, text_color)
            content_surface.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

            # Row divider
            if i < len(items) - 1:
                pygame.draw.line(content_surface, '#222222',
                                 (20, y + ROW_HEIGHT - 1),
                                 (self.popup_rect.width - 20, y + ROW_HEIGHT - 1), 1)

        # Blit only the visible window of the content surface
        scroll = self.scroll_offsets[self.active_tab]
        visible_area = pygame.Rect(0, scroll, self.popup_rect.width, self.content_height)
        screen.blit(content_surface, (self.popup_rect.left, self.content_top), visible_area)

    def draw(self, screen, money, purchased_upgrades):
        """Draw the shop button and popup if visible."""
        pygame.draw.rect(screen, 'black', self.button_rect)
        pygame.draw.rect(screen, 'white', self.button_rect, 2)
        btn_surface = self.font.render('Shop', True, 'white')
        screen.blit(btn_surface, btn_surface.get_rect(center=self.button_rect.center))

        if not self.visible:
            return

        # Popup background and border
        pygame.draw.rect(screen, 'black', self.popup_rect)
        pygame.draw.rect(screen, 'white', self.popup_rect, 2)

        # Title
        title = self.font.render('SHOP', True, 'white')
        screen.blit(title, title.get_rect(centerx=self.popup_rect.centerx, top=self.popup_rect.top + 15))

        # Tabs
        for tab_id, rect in self.tab_rects.items():
            is_active = self.active_tab == tab_id
            pygame.draw.rect(screen, '#222222' if is_active else 'black', rect)
            pygame.draw.rect(screen, 'white', rect, 2 if is_active else 1)
            label = tab_id.capitalize()
            tab_surf = self.small_font.render(label, True, 'white')
            screen.blit(tab_surf, tab_surf.get_rect(center=rect.center))

        # Divider below tabs
        pygame.draw.line(screen, 'grey',
                         (self.popup_rect.left + 20, self.popup_rect.top + 100),
                         (self.popup_rect.right - 20, self.popup_rect.top + 100), 1)

        # Scrollable content — clipped so rows can't bleed outside the popup
        screen.set_clip(self.content_rect)
        self._draw_tab_content(screen, money, purchased_upgrades)
        screen.set_clip(None)

        # Scroll indicator drawn after clip cleared so it sits on top of the border cleanly
        max_scroll = self._max_scroll(self.active_tab, purchased_upgrades)
        if max_scroll > 0:
            scroll = self.scroll_offsets[self.active_tab]
            total_height = len(self._visible_upgrades(purchased_upgrades) if self.active_tab == 'upgrades' else CONSUMABLES) * ROW_HEIGHT
            bar_height = max(20, int(self.content_height * (self.content_height / total_height)))
            bar_y = self.content_top + int((scroll / max_scroll) * (self.content_height - bar_height))
            bar_rect = pygame.Rect(self.popup_rect.right - 7, bar_y, 4, bar_height)
            pygame.draw.rect(screen, '#555555', bar_rect, border_radius=2)

        # Free guess indicator
        if self.free_guess_active:
            fg_surf = self.small_font.render('FREE GUESS ACTIVE', True, 'green')
            screen.blit(fg_surf, (self.popup_rect.left + 20, self.popup_rect.bottom - 55))

        # Close button — drawn after set_clip(None) so it's never clipped
        pygame.draw.rect(screen, 'black', self.close_rect)
        pygame.draw.rect(screen, 'white', self.close_rect, 2)
        close_surf = self.font.render('Close', True, 'white')
        screen.blit(close_surf, close_surf.get_rect(center=self.close_rect.center))