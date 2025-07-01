import pygame
import random

from machines.machine import Machine
from entities.item import Item
class Generator(Machine):
    def __init__(self, machine_data, rotation=0):
        self.image = machine_data.image
        self.size = machine_data.size
        self.rotation = rotation
        self.produced_letter=None

        self.production_interval = 1.0  # seconds between productions
        self.time_since_last_production = 0.0

        super().__init__(size=self.size, image=self.image, rotation=rotation)
    

    def produce_item(self, position=(0, 0)):
        if self.produced_letter is None:
            return None
        return Item(formula=self.produced_letter, is_theorem=False, position=position)
    

    def change_letter(self, new_letter):
        """ Change the letter produced by the generator and update the image accordingly. """
        self.produced_letter = new_letter
        """ this does not work currently.
        font = pygame.font.SysFont(None, 34)
        text_surface = font.render(self.produced_letter, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2+13))
        self.image = pygame.image.load("assets/sprites/generator.png").convert_alpha()  # Reload the base image
        self.image.blit(text_surface, text_rect)"""

    
    def update(self, dt):
        """Call this every frame with dt = time elapsed since last call in seconds."""
        if self.produced_letter is None:
            return None

        self.time_since_last_production += dt

        if self.time_since_last_production >= self.production_interval:
            self.time_since_last_production -= self.production_interval

            # For now, just produce at a random position
            new_item = self.produce_item(position=(random.randint(0, 1000), random.randint(0, 1000)))
            return new_item

        return None