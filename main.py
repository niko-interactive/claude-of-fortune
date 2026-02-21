import pygame
import random

from constants import SCREEN_SIZE
from puzzles import PUZZLES

from alphabet import Alphabet
from phrase import Phrase
from popup import Popup
from streak import Streak
from strikes import Strikes
from topic import Topic
from upgrades import Upgrades


# Scrabble values used to weight letter rarity in difficulty calculation
SCRABBLE = {
    'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1,
    'N': 1, 'R': 1, 'S': 1, 'T': 1, 'L': 1, 'H': 1,
    'D': 2, 'G': 2,
    'B': 3, 'C': 3, 'M': 3, 'P': 3,
    'F': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5,
    'J': 8, 'X': 8,
    'Q': 10, 'Z': 10
}

# For "What Are You Doing?" puzzles, I, N, G are removed from the difficulty
# calculation since every puzzle in this category ends in ING — effectively free letters
FREE_LETTERS_BY_CATEGORY = {
    'What Are You Doing?': {'I', 'N', 'G'}
}


def calculate_difficulty(phrase, category):
    """
    Calculate a numeric difficulty score for a puzzle.
    Formula: (unique_letters * rarity * avg_word_length) / num_words

    For categories with known free letters (e.g. What Are You Doing? always
    ends in ING), those letters are excluded from the unique set before scoring.
    """
    unique_letters = set(phrase.replace(' ', ''))

    # Remove any letters that are effectively free for this category
    free = FREE_LETTERS_BY_CATEGORY.get(category, set())
    unique_letters -= free

    rarity = sum(SCRABBLE[c] for c in unique_letters)
    words = phrase.split()
    avg_word_length = sum(len(w) for w in words) / len(words)
    num_words = len(words)
    return (len(unique_letters) * rarity * avg_word_length) / num_words


def get_max_difficulty(streak_count):
    """
    Return the maximum allowed puzzle difficulty based on the current streak.
    Difficulty gates open gradually as the player builds their streak:
      Streak 0-2:  max 200  (~54 puzzles available)
      Streak 3-4:  max 350  (~127 puzzles available)
      Streak 5-6:  max 500  (~174 puzzles available)
      Streak 7-8:  max 700  (~208 puzzles available)
      Streak 9+:   no limit (all 274 puzzles available)
    """
    if streak_count >= 9:
        return float('inf')
    elif streak_count >= 7:
        return 700
    elif streak_count >= 5:
        return 500
    elif streak_count >= 3:
        return 350
    else:
        return 200


def reset_game(font, streak, upgrades):
    """
    Set up a fresh round of the game.
    Filters available puzzles based on the player's current streak tier,
    selects one randomly, rebuilds all game objects, and applies upgrades.
    """
    max_difficulty = get_max_difficulty(streak.count)

    # Filter puzzles to those within the allowed difficulty for this streak
    available = [(text, topic) for text, topic in PUZZLES
                 if calculate_difficulty(text, topic) <= max_difficulty]

    # Fallback to all puzzles if the filter somehow produces an empty pool
    if not available:
        available = PUZZLES

    text, topic_text = random.choice(available)
    phrase = Phrase(text, font, *SCREEN_SIZE)
    alphabet = Alphabet(font, *SCREEN_SIZE)

    # Max strikes depends on which strike upgrades the player has unlocked
    max_strikes = upgrades.max_strikes(streak.count)
    strikes = Strikes(font, SCREEN_SIZE[0], max_strikes)
    topic = Topic(topic_text, font, *SCREEN_SIZE)

    # Position the topic label just below the bottom of the phrase
    if phrase.letters:
        bottom = max(letter.rect.bottom for letter in phrase.letters)
        topic.update_position(bottom)

    # Apply auto-guess upgrades silently — these do not count as player guesses
    # and will never add a strike even if the letter is not in the phrase
    auto_guesses = upgrades.get_auto_guesses(phrase.word, streak.count)
    for letter in auto_guesses:
        phrase.guess(letter)
        alphabet.guess(letter)

    return phrase, alphabet, strikes, topic


# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Word Game')
clock = pygame.time.Clock()
running = True

# Shared font used across all game objects
font = pygame.font.SysFont('Arial', 32)

# These persist across rounds — streak and upgrades are not reset between games
streak = Streak(font)
upgrades = Upgrades(font, *SCREEN_SIZE)

# Start the first round
phrase, alphabet, strikes, topic = reset_game(font, streak, upgrades)
popup = None  # Holds the active win/lose popup, or None if no popup is showing


# --- Game Loop ---
while running:
    for event in pygame.event.get():

        # Window close button
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If a popup is showing, check if the Play Again button was clicked
            if popup and popup.handle_click(event.pos):
                phrase, alphabet, strikes, topic = reset_game(font, streak, upgrades)
                popup = None
            else:
                # Otherwise pass the click to the upgrades button/menu
                upgrades.handle_click(event.pos, streak.count)

        if event.type == pygame.KEYDOWN:
            # Enter closes whichever overlay is currently open
            if event.key == pygame.K_RETURN:
                if popup:
                    phrase, alphabet, strikes, topic = reset_game(font, streak, upgrades)
                    popup = None
                elif upgrades.visible:
                    upgrades.visible = False

        # Only accept letter guesses when no overlay is open
        if event.type == pygame.KEYDOWN and popup is None and not upgrades.visible:
            if event.unicode.isalpha():
                letter = event.unicode.upper()

                # Ignore letters that have already been guessed
                if letter not in alphabet.guessed:
                    matched = phrase.guess(letter)
                    alphabet.guess(letter)

                    # Wrong guess costs a strike
                    if not matched:
                        strikes.add_strike()

                    # Check win/lose conditions after each guess
                    if phrase.is_solved():
                        streak.win()
                        popup = Popup('You Win!', font, *SCREEN_SIZE, phrase=phrase.word)
                    elif strikes.is_game_over():
                        streak.lose()
                        popup = Popup('You Lose!', font, *SCREEN_SIZE, phrase=phrase.word, streak=streak.previous)

    # --- Drawing ---
    screen.fill('black')
    phrase.draw(screen)
    alphabet.draw(screen)
    strikes.draw(screen)
    topic.draw(screen)
    streak.draw(screen)
    upgrades.draw(screen, streak.count)

    # Draw popup on top of everything else if one is active
    if popup:
        popup.draw(screen)

    pygame.display.update()

    # Cap at 30fps — no animation in this game so 60fps is unnecessary
    clock.tick(30)

pygame.quit()