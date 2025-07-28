import pygame
from gui.elements.button import Button
from gui.button_color_scheme import RED_COLORS

class AbstractMenu:
    PADDING = 10
    BG_COLOR = (30, 30, 30)
    BORDER_COLOR = (200, 200, 200)
    BORDER_WIDTH = 2
    CLOSE_BTN_SIZE = 30
    CLOSE_BTN_COLOR = (200, 50, 50)
    CLOSE_BTN_HOVER_COLOR = (255, 80, 80)

    def __init__(self, screen, size):
        """
        screen: pygame display surface
        size: (width, height) tuple for menu size
        """
        self.screen = screen
        self.size = size
        self.closed = False

        # Center menu rect on screen
        screen_rect = screen.get_rect()
        self.rect = pygame.Rect(
            (screen_rect.width - size[0]) // 2,
            (screen_rect.height - size[1]) // 2,
            size[0],
            size[1]
        )

        # Close button rect (top-right inside menu)
        self.close_rect = pygame.Rect(
            self.rect.right - self.PADDING - self.CLOSE_BTN_SIZE,
            self.rect.y + self.PADDING,
            self.CLOSE_BTN_SIZE,
            self.CLOSE_BTN_SIZE
        )
        self.close_button = Button(
            rect=self.close_rect,
            text="X",
            callback=self._close_menu,
            font=pygame.font.SysFont(None, 22),
            colors=RED_COLORS
        )

        self.font = pygame.font.SysFont(None, 20)

    def set_machine(self, generator_instance):
        self.generator = generator_instance

    def handle_events(self, events):
        self.close_button.handle_events(events)

    def update(self):
        self.close_button.update()
    
    def _close_menu(self):
        self.closed = True

    def draw(self):
        # Draw background panel
        pygame.draw.rect(self.screen, self.BG_COLOR, self.rect)
        # Draw border
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.rect, self.BORDER_WIDTH)

        # Draw close button (a red square with an X)
        self.close_button.draw(self.screen)