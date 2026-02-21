import pygame
from constants import LETTER_SLOT_WIDTH, LETTER_SLOT_HEIGHT, GAP
from letter import Letter


class Phrase:
    def __init__(self, word, font, screen_width, screen_height):
        self.word = word.upper()
        self.letters = []
        self.font = font

        space_width = 24
        padding = 40
        available_width = screen_width - padding

        # Split the phrase into lines that fit the screen
        lines = []
        current_line = []
        current_width = 0

        for char in self.word:
            char_width = space_width if char == ' ' else LETTER_SLOT_WIDTH
            added_width = char_width + GAP

            if current_width + added_width > available_width and current_line:
                if char == ' ':
                    lines.append(current_line)
                    current_line = []
                    current_width = 0
                else:
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

        if current_line:
            lines.append(current_line)

        # Strip leading/trailing spaces from each line
        lines = [[c for c in line if not (c == ' ' and (line.index(c) == 0 or line.index(c) == len(line) - 1))] for line in lines]

        # Calculate total block height to center vertically
        num_lines = len(lines)
        line_gap = 20
        total_height = num_lines * LETTER_SLOT_HEIGHT + (num_lines - 1) * line_gap
        start_y = (screen_height - total_height) // 2

        for line_index, line in enumerate(lines):
            line_width = sum(space_width if c == ' ' else LETTER_SLOT_WIDTH for c in line) + (len(line) - 1) * GAP
            start_x = (screen_width - line_width) // 2
            y = start_y + line_index * (LETTER_SLOT_HEIGHT + line_gap)

            x = start_x
            for char in line:
                if char == ' ':
                    x += space_width + GAP
                else:
                    self.letters.append(Letter(x, y, font))
                    x += LETTER_SLOT_WIDTH + GAP

    def guess(self, letter):
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
        return all(letter.letter is not None for letter in self.letters)

    def draw(self, screen):
        for letter in self.letters:
            letter.draw(screen)
