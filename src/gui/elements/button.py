import pygame

class Button:
    def __init__(self, rect, text, callback, font, selected=False):
        self.rect = pygame.Rect(rect) # by passing a rect, we get size and position.
        self.text = text
        self.callback = callback
        self.font = font
        self.selected = selected

    def draw(self, surface):
        color = (100, 100, 255) if self.selected else (80, 80, 80)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
