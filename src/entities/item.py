import pygame
from core.utils import world_to_screen

class Item:
    def __init__(self, formula, is_theorem=False, position=(0, 0)):
        self.formula = formula # right now, it is just a str. Later, i will implement a formula-class.
        self.is_theorem = is_theorem # There are 2 types of items: formulas and theorems
        self.position = pygame.Vector2(position)
        self.font = pygame.font.SysFont(None, 28)
        self.color = (200, 200, 255) if is_theorem else (255, 255, 255)
        self.radius = 20  # For example, draw as circle

    def update(self, dt):
        # example: update the position, if the item is on a belt.
        pass

    def draw(self, screen, camera):
        # Draw a circle with the formula text centered
        # TODO: This is not possible, if the formulas are big.
        # Idea: procedually generate an icon based on the formula. 
        # So you can still distinguish different formulas.
        screen_x, screen_y = world_to_screen(self.position.x, self.position.y, camera)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        text_surf = self.font.render(self.formula, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(screen_x, screen_y))
        screen.blit(text_surf, text_rect)