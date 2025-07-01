from machines.menu.abstract_menu import AbstractMenu
import pygame

class GeneratorMenu(AbstractMenu):
    def __init__(self, screen, size, generator_instance):
        super().__init__(screen, size)
        self.generator = generator_instance
        self.font = pygame.font.SysFont(None, 20)

    def handle_event(self, event):
        super().handle_event(event)
        print(self.generator)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pass
                # Handle clicks on buttons or controls here

    def draw(self):
        super().draw()