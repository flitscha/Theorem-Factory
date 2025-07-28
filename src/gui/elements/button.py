import pygame
from gui.button_color_scheme import DEFAULT_COLORS

class Button:
    """Standard Button - is triggered when the mouse button is released"""
    
    def __init__(self, rect, text, callback, font, selected=False, colors=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.selected = selected # used for toggle-buttons
        self.colors = colors or DEFAULT_COLORS
        self.is_pressed = False # this means, the mouse is currently pressed (on the button)
        self.is_hovered = False
        
    def update(self, mouse_pos=None):
        """Update hover state based of the mouse-position"""
        if not mouse_pos:
            mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def toggle(self):
        self.selected = not self.selected
        
    def set_selected(self, selected):
        self.selected = selected

    def draw(self, surface):
        # color based on the state
        if self.is_pressed:
            color = self.colors.pressed
        elif self.selected:
            if self.is_hovered:
                color = self.colors.selected_hover
            else:
                color = self.colors.selected
        else:
            if self.is_hovered:
                color = self.colors.hover
            else:
                color = self.colors.normal

        # draw button
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)
        
        # draw text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos): # left mouse button
                    self.is_pressed = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.is_pressed: # left mouse button
                    self.is_pressed = False
                    if self.rect.collidepoint(event.pos): # Only trigger, if mouse still on button
                        self.callback()