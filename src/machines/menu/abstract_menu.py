import pygame

class AbstractMenu:
    PADDING = 10
    BG_COLOR = (30, 30, 30)
    BORDER_COLOR = (200, 200, 200)
    BORDER_WIDTH = 2
    CLOSE_BTN_SIZE = 20
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

        self.font = pygame.font.SysFont(None, 20)

    def set_machine(self, generator_instance):
        self.generator = generator_instance

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                self.closed = True

    def update(self):
        pass

    def draw(self):
        # Draw background panel
        pygame.draw.rect(self.screen, self.BG_COLOR, self.rect)
        # Draw border
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.rect, self.BORDER_WIDTH)

        # Draw close button (a red square with an X)
        mouse_pos = pygame.mouse.get_pos()
        if self.close_rect.collidepoint(mouse_pos):
            color = self.CLOSE_BTN_HOVER_COLOR
        else:
            color = self.CLOSE_BTN_COLOR

        pygame.draw.rect(self.screen, color, self.close_rect)

        # Draw 'X' on close button
        padding = 4
        start_pos1 = (self.close_rect.left + padding, self.close_rect.top + padding)
        end_pos1 = (self.close_rect.right - padding, self.close_rect.bottom - padding)
        start_pos2 = (self.close_rect.left + padding, self.close_rect.bottom - padding)
        end_pos2 = (self.close_rect.right - padding, self.close_rect.top + padding)

        pygame.draw.line(self.screen, (255, 255, 255), start_pos1, end_pos1, 2)
        pygame.draw.line(self.screen, (255, 255, 255), start_pos2, end_pos2, 2)

        # Placeholder title
        title = self.font.render("Base Menu", True, (255, 255, 255))
        self.screen.blit(title, (self.rect.x + self.PADDING*2 + self.CLOSE_BTN_SIZE, self.rect.y + self.PADDING))