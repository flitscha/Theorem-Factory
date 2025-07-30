from gui.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button

class ControlsMenu(AbstractMenu):
    def __init__(self, screen, on_back):
        super().__init__(screen, width=800, height=600, on_back=on_back, title="Controls")

        self.controls_text = [
            "WASD / Arrow Keys - Move camera",
            "Right Mouse Button (hold) - Drag camera",
            "Mouse Wheel - Zoom in/out",
            "Left Mouse Button - Place machine",
            "Q - Select machine under cursor",
            "R - Rotate machine",
            "Shift (hold) - Temporary erase tool",
            "ESC - Open/close pause menu"
        ]

        self.buttons = self._create_buttons()

    def _create_buttons(self):
        button_width = 250
        button_height = 50
        back_btn = Button(
            (self.menu_x + 40, self.menu_y + self.height - button_height - 40, button_width, 50),
            "Back",
            self.on_back,
            self.font
        )
        return [back_btn]

    def draw(self):
        super().draw()

        if not self.is_open or self.active_submenu:
            return

        start_y = self.menu_y + 100
        line_spacing = 40
        for i, line in enumerate(self.controls_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.menu_x + 60, start_y + i * line_spacing))
