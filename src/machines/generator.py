import pygame

from machines.machine import Machine

class Generator(Machine):
    def __init__(self, machine_database, rotation=0):
        data = machine_database.get("generator")
        self.image = data.image
        self.size = data.size
        self.rotation = rotation
        self.produced_letter=None

        super().__init__(size=self.size, image=self.image, rotation=rotation)
    

    def change_letter(self, new_letter):
        """ Change the letter produced by the generator and update the image accordingly. """
        self.produced_letter = new_letter
        font = pygame.font.SysFont(None, 34)
        text_surface = font.render(self.produced_letter, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2+13))
        self.image = pygame.image.load("assets/sprites/generator.png").convert_alpha()  # Reload the base image
        self.image.blit(text_surface, text_rect)