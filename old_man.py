import pygame


class OldMan:
    """
    Full-screen overlay showing a stick-figure old man with a dialogue box.
    Styled to match the shop/popup aesthetic: black fill, white border.

    The message string can be swapped at any time via old_man.message = '...'.
    Visibility is toggled by setting old_man.visible = True/False, or via
    handle_click() which closes the panel when the Close button is pressed.

    Usage in main.py:
        old_man = OldMan(font, *SCREEN_SIZE)
        # open it:
        old_man.visible = True
        # each frame:
        old_man.draw(screen)
        # in event loop (before other click handling):
        if old_man.handle_click(event.pos):
            pass  # click was consumed
    """

    PANEL_W = 520
    PANEL_H = 400

    def __init__(self, font, screen_width, screen_height):
        self.font       = font
        self.small_font = pygame.font.SysFont('Arial', 22)
        self.screen_w   = screen_width
        self.screen_h   = screen_height

        self.visible = False
        self.message = "Oh, you saved me! Thank you! But, wait... WHERE IS MY HAT??"

        # Main panel — centred on screen
        self.panel_rect = pygame.Rect(0, 0, self.PANEL_W, self.PANEL_H)
        self.panel_rect.center = (screen_width // 2, screen_height // 2)

        # Close button — pinned to bottom of panel
        self.close_rect = pygame.Rect(0, 0, 140, 44)
        self.close_rect.centerx = self.panel_rect.centerx
        self.close_rect.bottom  = self.panel_rect.bottom - 18

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def handle_click(self, pos):
        """
        If the overlay is visible, consume the click.
        Closes the panel when Close is pressed.
        Returns True if visible (click was consumed), False otherwise.
        """
        if not self.visible:
            return False
        if self.close_rect.collidepoint(pos):
            self.visible = False
        return True  # always consume clicks while open

    def draw(self, screen):
        if not self.visible:
            return

        # Dim the game behind the panel
        dim = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        screen.blit(dim, (0, 0))

        # Panel background + border
        pygame.draw.rect(screen, 'black', self.panel_rect)
        pygame.draw.rect(screen, 'white', self.panel_rect, 2)

        # Title
        title = self.font.render('OLD MAN', True, 'white')
        screen.blit(title, title.get_rect(
            centerx=self.panel_rect.centerx,
            top=self.panel_rect.top + 16,
        ))

        # Divider below title
        div_y = self.panel_rect.top + 58
        pygame.draw.line(screen, '#444444',
                         (self.panel_rect.left + 20, div_y),
                         (self.panel_rect.right - 20, div_y), 1)

        # ------------------------------------------------------------------
        # Stick figure
        # ------------------------------------------------------------------
        cx      = self.panel_rect.centerx
        fig_top = div_y + 18

        # Head
        head_r = 20
        head_c = (cx, fig_top + head_r)
        pygame.draw.circle(screen, 'white', head_c, head_r, 2)

        # Body
        body_top    = head_c[1] + head_r
        body_bottom = body_top + 52
        pygame.draw.line(screen, 'white', (cx, body_top), (cx, body_bottom), 2)

        # Arms — angled downward to look tired/old
        arm_y = body_top + 18
        pygame.draw.line(screen, 'white', (cx, arm_y), (cx - 34, arm_y + 20), 2)
        pygame.draw.line(screen, 'white', (cx, arm_y), (cx + 34, arm_y + 20), 2)

        # Legs
        leg_bottom = body_bottom + 44
        pygame.draw.line(screen, 'white', (cx, body_bottom), (cx - 22, leg_bottom), 2)
        pygame.draw.line(screen, 'white', (cx, body_bottom), (cx + 22, leg_bottom), 2)

        # Walking stick on the right side
        stick_top_x = cx + 34
        stick_top_y = arm_y + 20
        pygame.draw.line(screen, 'white',
                         (stick_top_x, stick_top_y),
                         (stick_top_x + 8, leg_bottom), 2)

        # ------------------------------------------------------------------
        # Dialogue box — sits just below the figure's feet
        # ------------------------------------------------------------------
        dlg_top  = leg_bottom + 16
        dlg_rect = pygame.Rect(
            self.panel_rect.left  + 24,
            dlg_top,
            self.panel_rect.width - 48,
            76,
        )
        pygame.draw.rect(screen, '#000000', dlg_rect)
        pygame.draw.rect(screen, '#666666', dlg_rect, 1)

        self._draw_wrapped(screen, self.message, dlg_rect)

        # Close button
        pygame.draw.rect(screen, 'black', self.close_rect)
        pygame.draw.rect(screen, 'white', self.close_rect, 2)
        close_surf = self.font.render('Close', True, 'white')
        screen.blit(close_surf, close_surf.get_rect(center=self.close_rect.center))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _draw_wrapped(self, screen, text, rect):
        """Word-wrap text to fit inside rect and centre it vertically."""
        words = text.split()
        lines = []
        line  = ''
        for word in words:
            test = (line + ' ' + word).strip()
            if self.small_font.size(test)[0] <= rect.width - 16:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)

        lh      = self.small_font.get_linesize()
        total_h = len(lines) * lh
        y       = rect.top + max(0, (rect.height - total_h) // 2)

        for i, ln in enumerate(lines):
            surf = self.small_font.render(ln, True, '#DDDDDD')
            screen.blit(surf, surf.get_rect(centerx=rect.centerx, top=y + i * lh))
