import pygame


class Topic:
    def __init__(self, topic, font, screen_width, screen_height):
        self.font = font
        self.topic = topic.upper()
        self.screen_width = screen_width
        self.y = screen_height // 2 + 60

    def update_position(self, bottom_of_phrase):
        self.y = bottom_of_phrase + 20

    def draw(self, screen):
        surface = self.font.render(self.topic, True, 'white')
        topic_rect = surface.get_rect(centerx=self.screen_width // 2, top=self.y)
        screen.blit(surface, topic_rect)
