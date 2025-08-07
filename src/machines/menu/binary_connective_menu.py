import pygame
from machines.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button
from machines.types.binary_connective import BinaryConnectiveType

class BinaryConnectiveMenu(AbstractMenu):
    def __init__(self, screen, size, machine_instance):
        super().__init__(screen, size)
        self.machine = machine_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 22)
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        margin = 10
        btn_width = 100
        btn_height = 40
        start_x = self.rect.centerx - (btn_width * 1.5 + margin)
        start_y = self.rect.y + 90

        self.buttons.clear()

        for i, connective in enumerate(BinaryConnectiveType):
            x = start_x + i * (btn_width + margin)
            y = start_y

            callback = self._create_connective_callback(connective)
            selected = (connective == self.machine.selected_connective)

            btn = Button(
                rect=(x, y, btn_width, btn_height),
                text=connective.name,
                callback=callback,
                font=self.font,
                selected=selected
            )
            self.buttons.append(btn)

    def _create_connective_callback(self, connective):
        def callback():
            self.machine.selected_connective = connective
            self._update_button_selection()
        return callback

    def _update_button_selection(self):
        for btn in self.buttons:
            btn.set_selected(btn.text == self.machine.selected_connective.name)

    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse_pos)

    def handle_events(self, events):
        super().handle_events(events)
        for btn in self.buttons:
            btn.handle_events(events)

    def draw(self):
        super().draw()
        title_text = self.font.render("Connective Settings", True, (255, 255, 255))
        self.screen.blit(title_text, (self.rect.x + self.PADDING, self.rect.y + 10))

        instruction = self.small_font.render("Select a logical connective:", True, (180, 180, 180))
        self.screen.blit(instruction, (self.rect.x + self.PADDING, self.rect.y + 50))

        for btn in self.buttons:
            btn.draw(self.screen)
