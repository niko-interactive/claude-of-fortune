from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP
from letter import Letter


class Phrase:
    """
    Represents the secret phrase the player is trying to guess.
    Breaks the phrase into lines that fit the screen width, centers
    them vertically, and manages a Letter slot for each non-space character.
    """

    def __init__(self, word, font, screen_width, screen_height):
        self.word = word.upper()
        self.letters = []  # One Letter object per non-space character
        self.font = font

        space_width = 24   # Visual gap width used to represent a space between words
        padding = 40       # Total horizontal padding to keep letters off screen edges
        available_width = screen_width - padding

        # --- Line Wrapping ---
        # Walk through each character and build lines that fit within available_width.
        # When a line would overflow, walk back to the last space to avoid breaking mid-word.
        lines = []
        current_line = []
        current_width = 0

        for char in self.word:
            char_width = space_width if char == ' ' else LETTER_SLOT_WIDTH
            added_width = char_width + GAP

            if current_width + added_width > available_width and current_line:
                if char == ' ':
                    # Space caused the overflow — start a new line and discard the space
                    lines.append(current_line)
                    current_line = []
                    current_width = 0
                else:
                    # Non-space caused the overflow — walk back to the last space to wrap cleanly
                    split = len(current_line) - 1
                    while split > 0 and current_line[split] != ' ':
                        split -= 1
                    next_line = current_line[split + 1:]
                    current_line = current_line[:split]
                    lines.append(current_line)
                    current_line = next_line
                    current_width = sum((space_width if c == ' ' else LETTER_SLOT_WIDTH) + GAP for c in current_line)
                    current_line.append(char)
                    current_width += char_width + GAP
            else:
                current_line.append(char)
                current_width += added_width

        # Add the last line if anything remains
        if current_line:
            lines.append(current_line)

        # Remove any leading or trailing spaces from each line left over from wrapping
        lines = [[c for c in line if not (c == ' ' and (line.index(c) == 0 or line.index(c) == len(line) - 1))] for line in lines]

        # --- Vertical Centering ---
        # Calculate the total height of all lines combined and center the block on screen
        num_lines = len(lines)
        line_gap = 20
        total_height = num_lines * LETTER_SLOT_HEIGHT + (num_lines - 1) * line_gap
        start_y = (screen_height - total_height) // 2

        # --- Build Letter Objects ---
        # For each line, calculate its width, center it horizontally,
        # then create a Letter object for each non-space character
        for line_index, line in enumerate(lines):
            line_width = sum(space_width if c == ' ' else LETTER_SLOT_WIDTH for c in line) + (len(line) - 1) * GAP
            start_x = (screen_width - line_width) // 2
            y = start_y + line_index * (LETTER_SLOT_HEIGHT + line_gap)

            x = start_x
            for char in line:
                if char == ' ':
                    # Spaces advance the x position but don't create a Letter object
                    x += space_width + GAP
                else:
                    self.letters.append(Letter(x, y, font))
                    x += LETTER_SLOT_WIDTH + GAP

    def guess(self, letter):
        """
        Reveal all instances of the guessed letter in the phrase.
        Iterates over non-space characters only, matching against the
        corresponding Letter object by index. Returns True if at least
        one match was found, False otherwise.
        """
        matched = False
        non_space_index = 0
        for char in self.word:
            if char == ' ':
                continue
            if char == letter.upper():
                self.letters[non_space_index].letter = char
                matched = True
            non_space_index += 1
        return matched

    def is_solved(self):
        """Return True if every letter slot has been revealed."""
        return all(letter.letter is not None for letter in self.letters)

    def draw(self, screen):
        """Draw all letter slots to the screen."""
        for letter in self.letters:
            letter.draw(screen)