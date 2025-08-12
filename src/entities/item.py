import pygame
from core.utils import world_to_screen
from core.formula import Formula

class Item:
    def __init__(self, formula: Formula, is_theorem=False, position=(0, 0), assumptions=None):
        self.formula = formula
        self.is_theorem = is_theorem # There are 2 types of items: formulas and theorems
        self.assumptions = set() if assumptions is None else set(assumptions) # Theorems can depend on assumptions
        self.position = pygame.Vector2(position)
        self.font = pygame.font.SysFont(None, 28)
        self.color = (200, 200, 255) if is_theorem else (255, 255, 255)
        self.radius = 10
        self.font_size = 15

        # generate the text only once to save computing time
        font = pygame.font.SysFont("arial", self.font_size*10, bold=True)
        self.text_surface = font.render(str(self.formula), True, (0, 0, 0))

    def update(self, dt):
        # example: update the position, if the item is on a belt.
        pass


    def draw(self, screen, camera):
        # Draw a circle with the formula text centered
        # TODO: This is not possible, if the formulas are big.
        # Idea: procedually generate an icon based on the formula. 
        # So you can still distinguish different formulas.
        screen_x, screen_y = world_to_screen(self.position.x, self.position.y, camera)
        radius = int(self.radius * camera.zoom)

        # choose color
        color = (240, 200, 80)

        # draw shape
        if self.is_theorem:
            pygame.draw.rect(screen, color, (screen_x-radius, screen_y-radius, 2*radius, 2*radius))
        else:
            pygame.draw.circle(screen, color, (screen_x, screen_y), radius)

        scaled_text = pygame.transform.smoothscale(
            self.text_surface,
            (int(self.text_surface.get_width() * camera.zoom / 10),
             int(self.text_surface.get_height() * camera.zoom) / 10)
        )

        text_rect = scaled_text.get_rect(center=(screen_x, screen_y))
        screen.blit(scaled_text, text_rect)
