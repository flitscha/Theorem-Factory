import pygame
from machines.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button

class AndEliminationMenu(AbstractMenu):
    """
    Simple menu to choose which conjunct to output (Left / Right).
    Default: Left selected.
    """
    def __init__(self, screen, size, machine_instance):
        super().__init__(screen, size)
        self.machine = machine_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 20)

        btn_w = 120
        btn_h = 40
        gap = 12
        center_x = self.rect.centerx
        y = self.rect.y + 90

        # left button
        left_rect = (center_x - btn_w - gap//2, y, btn_w, btn_h)
        self.left_button = Button(
            rect=left_rect,
            text="Left",
            callback=lambda: self._set_side(0),
            font=self.small_font,
            selected=(self.machine.get_output_side() == 'left')
        )

        # right button
        right_rect = (center_x + gap//2, y, btn_w, btn_h)
        self.right_button = Button(
            rect=right_rect,
            text="Right",
            callback=lambda: self._set_side(1),
            font=self.small_font,
            selected=(self.machine.get_output_side() == 'right')
        )

    def _set_side(self, index):
        self.machine.set_output_side(index)
        self._update_button_states()

    def _update_button_states(self):
        self.left_button.set_selected(self.machine.get_output_side() == 'left')
        self.right_button.set_selected(self.machine.get_output_side() == 'right')

    def update(self):
        super().update()
        mouse_pos = pygame.mouse.get_pos()
        self.left_button.update(mouse_pos)
        self.right_button.update(mouse_pos)

    def handle_events(self, events):
        super().handle_events(events)
        self.left_button.handle_events(events)
        self.right_button.handle_events(events)

    def draw(self):
        super().draw()
        # Title
        title = self.font.render("And-Elimination", True, (255,255,255))
        self.screen.blit(title, (self.rect.x + self.PADDING, self.rect.y + 10))

        # Instruction
        instr = self.small_font.render("Select which conjunct the machine should output:", True, (200,200,200))
        self.screen.blit(instr, (self.rect.x + self.PADDING, self.rect.y + 50))

        # Draw buttons
        self.left_button.draw(self.screen)
        self.right_button.draw(self.screen)

        # small hint about requirement
        hint = self.small_font.render("Input must be a THEOREM of the form (A * B).", True, (150,150,150))
        self.screen.blit(hint, (self.rect.x + self.PADDING, self.rect.y + 150))
