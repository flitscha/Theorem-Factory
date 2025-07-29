from config.constants import *
from gui.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button
from config.settings_manager import settings_manager
from gui.button_color_scheme import GREEN_COLORS


class DebugSettingsMenu(AbstractMenu):
    def __init__(self, screen, on_back, debug_system=None):
        super().__init__(screen, width=800, height=600, on_back=on_back, title="Debug Settings")

        # Create buttons
        self.buttons = self._create_buttons()

        # Submenus

    def _create_buttons(self):
        buttons = []
        # TODO: get rid of the magic numbers
        toggle_button_width = 40
        button_width = 300 # normal buttons. (for example the back-button)
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 120
        button_x = self.menu_x + self.width - 200
        
        # list of the settings. (settings that are ON / OFF)
        settings_list = [
            ("debug.show_fps", "FPS"),
            ("debug.show_coords", "Coords"),
            ("debug.show_ports", "Ports")
        ]

        for i, (path, label) in enumerate(settings_list):
            y_pos = start_y + i * button_spacing

            # create the toggle-buttons. (no text. We create the text in the draw-function) 
            btn = Button(
                (button_x, y_pos, toggle_button_width, toggle_button_width), # square buttons
                "",
                lambda p=path, idx=i: self._toggle_setting(p, idx),
                self.font,
                selected=settings_manager.get(path),
                colors=GREEN_COLORS
            )
            buttons.append(btn)
        
        # Back button
        back_btn = Button(
            (self.menu_x + 40, self.menu_y + self.height - button_height - 40, button_width, 50),
            "Back",
            self.on_back,
            self.font
        )
        buttons.append(back_btn)

        # save the labels for drawing
        self.setting_labels = [label for _, label in settings_list]
        return buttons

    def _toggle_setting(self, path, button_index):
        settings_manager.toggle(path)
        self.buttons[button_index].set_selected(settings_manager.get(path))

    def draw(self):
        super().draw()

        # draw labels left of the buttons
        if not self.is_open or self.active_submenu:
            return

        button_width = 50
        button_spacing = 60
        start_y = self.menu_y + 120
        label_x = self.menu_x + 150

        for i, label in enumerate(self.setting_labels):
            y_pos = start_y + i * button_spacing + button_width // 4
            text_surface = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(text_surface, (label_x, y_pos))

