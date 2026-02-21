import pygame
import random
from constants import SCREEN_SIZE
from phrase import Phrase
from alphabet import Alphabet
from strikes import Strikes
from popup import Popup
from topic import Topic
from puzzles import PUZZLES
from streak import Streak


def reset_game(font, streak):
    text, topic_text = random.choice(PUZZLES)
    phrase = Phrase(text, font, *SCREEN_SIZE)
    alphabet = Alphabet(font, *SCREEN_SIZE)
    strikes = Strikes(font, SCREEN_SIZE[0])
    topic = Topic(topic_text, font, *SCREEN_SIZE)

    if phrase.letters:
        bottom = max(letter.rect.bottom for letter in phrase.letters)
        topic.update_position(bottom)

    return phrase, alphabet, strikes, topic


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Claude of Fortune')
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont('Arial', 32)
streak = Streak(font)
phrase, alphabet, strikes, topic = reset_game(font, streak)
popup = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if popup and popup.handle_click(event.pos):
                phrase, alphabet, strikes, topic = reset_game(font, streak)
                popup = None

        if event.type == pygame.KEYDOWN and popup is None:
            if event.unicode.isalpha():
                letter = event.unicode.upper()
                if letter not in alphabet.guessed:
                    matched = phrase.guess(letter)
                    alphabet.guess(letter)
                    if not matched:
                        strikes.add_strike()

                    if phrase.is_solved():
                        streak.win()
                        popup = Popup('You Win!', font, *SCREEN_SIZE, phrase=phrase.word)
                    elif strikes.is_game_over():
                        streak.lose()
                        popup = Popup('You Lose!', font, *SCREEN_SIZE, phrase=phrase.word, streak=streak.previous)

    screen.fill('black')
    phrase.draw(screen)
    alphabet.draw(screen)
    strikes.draw(screen)
    topic.draw(screen)
    streak.draw(screen)
    if popup:
        popup.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()