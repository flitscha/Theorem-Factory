import pygame
from config.settings import *
from gui.elements.button import Button

class SettingsMenu:
    def __init__(self, screen, game_state_manager, on_back, debug_system=None):
        self.screen = screen
        self.game_state = game_state_manager
        self.on_back = on_back
        self.debug_system = debug_system
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.is_open = False

        # Layout
        self.menu_width = 800
        self.menu_height = 600
        self.menu_x = (SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_height) // 2

        # Buttons
        self.buttons = self._create_buttons()

    def _create_buttons(self):
        buttons = []
        button_width = 300
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 120

        # Back button
        back_btn = Button(
            (self.menu_x + 50, start_y, button_width, button_height),
            "Back",
            self._back_to_pause,
            self.font
        )
        buttons.append(back_btn)

        return buttons

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def _toggle_coords(self):
        self.debug_system.show_coordinates = not self.debug_system.show_coordinates
        self.buttons[0].text = f"Coords: {'ON' if self.debug_system.show_coordinates else 'OFF'}"

    def _toggle_fps(self):
        self.debug_system.show_fps = not self.debug_system.show_fps
        self.buttons[1].text = f"FPS: {'ON' if self.debug_system.show_fps else 'OFF'}"

    def _back_to_pause(self):
        self.on_back()

    def handle_events(self, events):
        if not self.is_open:
            return
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._back_to_pause()
        for button in self.buttons:
            button.handle_events(events)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def draw(self):
        if not self.is_open:
            return
        
        # Draw menu background
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(self.screen, (40, 40, 40), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 3)
        
        # Draw title
        title_text = self.title_font.render("SETTINGS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.menu_x + self.menu_width // 2, self.menu_y + 50))
        self.screen.blit(title_text, title_rect)

        # draw the buttons
        for button in self.buttons:
            button.draw(self.screen)
