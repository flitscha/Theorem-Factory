import pygame

class Tooltip:
    # A simple tooltip class to display text boxes near the mouse cursor
    def __init__(self, font, padding=10, bg_color=(40, 40, 40), text_color=(230, 230, 230)):
        self.font = font
        self.padding = padding
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_lines = []
        self.visible = False
        self.pos = (0, 0)

    def show(self, text_lines, pos):
        self.text_lines = text_lines
        self.pos = pos
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surface):
        if not self.visible or not self.text_lines:
            return

        rendered = [self.font.render(line, True, self.text_color) for line in self.text_lines]
        width = max(r.get_width() for r in rendered) + 2 * self.padding
        height = sum(r.get_height() for r in rendered) + 2 * self.padding

        x, y = self.pos
        # ensure tooltip stays within screen
        screen_rect = surface.get_rect()
        if x + width > screen_rect.right:
            x = screen_rect.right - width - 10
        if y + height > screen_rect.bottom:
            y = screen_rect.bottom - height - 10

        pygame.draw.rect(surface, self.bg_color, (x, y, width, height))
        pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 1)

        offset_y = y + self.padding
        for r in rendered:
            surface.blit(r, (x + self.padding, offset_y))
            offset_y += r.get_height()