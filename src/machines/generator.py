import pygame

from machines.machine import Machine

class Generator(Machine):
    def __init__(self):
        self.image = pygame.image.load("assets/sprites/generator.png").convert_alpha()
        super().__init__(size = 2, image = self.image)