import pygame
from machines.menu.elements.tool_tip import Tooltip


BASE_COLOR = (40, 120, 255)
HOVER_COLOR = (70, 150, 255)
TEXT_COLOR = (255, 255, 255)

class Info():
    def __init__(self, rect, text=""):
        self.rect = rect
        self.hovered = False
        
        self.i_font = pygame.font.SysFont(None, 24, bold=True)
        font = pygame.font.SysFont(None, 24)
        self.tooltip = Tooltip(font, line_spacing=6)
        self.text = text


    def update(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        self.hovered = self.rect.collidepoint(mouse_pos)

        # update Tooltip
        self.tooltip.hide()
        if self.hovered:
            self.tooltip.show(self.text, (mouse_pos[0] + 16, mouse_pos[1] + 12))


    def draw(self, surface):
        # draw circle
        color = HOVER_COLOR if self.hovered else BASE_COLOR
        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // 2
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, (255, 255, 255), center, radius, 2) # border

        # "i"
        text_surface = self.i_font.render("i", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)

        # draw the tooltip
        self.tooltip.draw(surface)
