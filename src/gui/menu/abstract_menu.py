import pygame
from config.constants import *

class AbstractMenu:
    def __init__(self, screen, width=800, height=600, on_back=None, title="MENU"):
        self.screen = screen
        self.width = width
        self.height=height
        self.on_back = on_back
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.is_open = False
        self.opened_this_frame = False # flank for is_open

        # layout
        self.menu_x = (SCREEN_WIDTH - self.width) // 2
        self.menu_y = (SCREEN_HEIGHT - self.height) // 2

        # submenu
        self.active_submenu = None

        # buttons
        self.buttons = []

        # title
        self.title = title

    # ---- lifecycle ----
    def open(self):
        self.is_open = True
        self.opened_this_frame = True

    def close(self):
        self.is_open = False

    # ---- submenus ----
    def open_submenu(self, submenu):
        self.active_submenu = submenu
        submenu.open()

    def close_submenu(self):
        if self.active_submenu:
            self.active_submenu.close()
            self.active_submenu = None

    # ---- drawing ----
    def draw(self):
        if not self.is_open:
            return

        # only draw the submenu, if active
        if self.active_submenu:
            self.active_submenu.draw()
            return

        # background
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.width, self.height)
        pygame.draw.rect(self.screen, (40, 40, 40), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 3)

        # title
        title_text = self.title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.menu_x + self.width // 2, self.menu_y + 50))
        self.screen.blit(title_text, title_rect)

        # buttons
        for button in self.buttons:
            button.draw(self.screen)

    # ---- events & update ----
    def handle_events(self, events):
        if not self.is_open or self.opened_this_frame:
            return

        if self.active_submenu:
            self.active_submenu.handle_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.on_back:
                    self.on_back()

        for button in self.buttons:
            button.handle_events(events)

    def update(self):
        if not self.is_open:
            self.opened_this_frame = False
            return

        if self.active_submenu:
            self.active_submenu.update()
            return

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
        
        self.opened_this_frame = False
        
