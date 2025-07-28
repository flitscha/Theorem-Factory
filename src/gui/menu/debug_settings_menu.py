import pygame
from config.settings import *
from gui.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button


class DebugSettingsMenu(AbstractMenu):
    def __init__(self, screen, on_back, debug_system=None):
        super().__init__(screen, width=800, height=600, on_back=on_back, title="Debug Settings")

        # Create buttons
        self.buttons = self._create_buttons()

        # Submenus

    def _create_buttons(self):
        buttons = []
        button_width = 250
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 120
        
        # Back button
        back_btn = Button(
            (self.menu_x + (self.width - button_width) // 2, start_y, button_width, button_height),
            "Back",
            self.on_back,
            self.font
        )
        buttons.append(back_btn)
        return buttons

    def _toggle_coords(self):
        self.debug_system.show_coordinates = not self.debug_system.show_coordinates
        self.buttons[0].text = f"Coords: {'ON' if self.debug_system.show_coordinates else 'OFF'}"

    def _toggle_fps(self):
        self.debug_system.show_fps = not self.debug_system.show_fps
        self.buttons[1].text = f"FPS: {'ON' if self.debug_system.show_fps else 'OFF'}"