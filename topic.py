import pygame


class Topic:
    """
    Displays the puzzle category label centered below the phrase,
    mimicking the category banner seen in Wheel of Fortune.
    """

    def __init__(self, topic, font, screen_width, screen_height):
        self.font = font
        self.topic = topic.upper()
        self.screen_width = screen_width

        # Default y position — will be overridden by update_position
        # once the phrase has been laid out and its bottom is known
        self.y = screen_height // 2 + 60

    def update_position(self, bottom_of_phrase):
        """
        Reposition the topic label just below the phrase.
        Called after the phrase is built so the exact bottom is known.
        """
        self.y = bottom_of_phrase + 20

    def draw(self, screen):
        """Draw the topic label centered horizontally below the phrase."""
        surface = self.font.render(self.topic, True, 'white')
        topic_rect = surface.get_rect(centerx=self.screen_width // 2, top=self.y)
        screen.blit(surface, topic_rect)