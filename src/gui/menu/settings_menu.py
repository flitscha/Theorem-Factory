from config.constants import *
from gui.elements.button import Button
from gui.menu.debug_settings_menu import DebugSettingsMenu
from gui.menu.abstract_menu import AbstractMenu

class SettingsMenu(AbstractMenu):
    def __init__(self, screen, on_back):
        super().__init__(screen, width=800, height=600, on_back=on_back, title="Settings")

        # Create buttons
        self.buttons = self._create_buttons()

        # Submenus
        self.debug_menu = DebugSettingsMenu(screen, on_back=self.close_submenu)


    def _create_buttons(self):
        buttons = []
        button_width = 250
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 120

        # Debug settings button
        debug_btn = Button(
            (self.menu_x + (self.width - button_width) // 2, start_y, button_width, button_height),
            "Debug Settings",
            self._open_debug,
            self.font
        )
        buttons.append(debug_btn)

        # back button
        back_btn = Button(
            (self.menu_x + 40, self.menu_y + self.height - button_height - 40, button_width, 50),
            "Back",
            self.on_back,
            self.font
        )
        buttons.append(back_btn)

        return buttons
    

    def _open_debug(self):
        """Open debug-settings menu"""
        self.open_submenu(self.debug_menu)
