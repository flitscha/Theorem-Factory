import string
import pygame
from machines.menu.abstract_menu import AbstractMenu
from gui.elements.button import Button

class GeneratorMenu(AbstractMenu):
    def __init__(self, screen, size, generator_instance):
        super().__init__(screen, size)
        self.generator = generator_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 22)
        self.letter_buttons = []
        self.create_letter_buttons()
    

    def create_letter_buttons(self):
        """Create 26 letter buttons, and set the one currently selected."""
        margin = 10
        btn_width = 40
        btn_height = 40
        cols = 9

        # Total grid size
        grid_width = cols * btn_width + (cols - 1) * margin
        rows = (len(string.ascii_lowercase) + cols - 1) // cols
        grid_height = rows * btn_height + (rows - 1) * margin

        start_x = self.rect.centerx - grid_width // 2
        start_y = self.rect.y + 90

        self.letter_buttons.clear()

        for i, letter in enumerate(string.ascii_lowercase):
            x = start_x + (i % cols) * (btn_width + margin)
            y = start_y + (i // cols) * (btn_height + margin)

            def make_callback(l=letter):
                return lambda: self.set_letter(l)

            selected = (letter == self.generator.produced_letter)
            btn = Button((x, y, btn_width, btn_height), letter, make_callback(), self.font, selected)
            self.letter_buttons.append(btn)

    def set_letter(self, letter):
        self.generator.produced_letter = letter
        self.update_button_selection()

    def update_button_selection(self):
        for btn in self.letter_buttons:
            btn.selected = (btn.text == self.generator.produced_letter)

    def handle_event(self, event):
        super().handle_event(event)
        for btn in self.letter_buttons:
            btn.handle_event(event)

    def draw(self):
        super().draw()

        # Draw heading
        title_text = self.font.render("Generator Settings", True, (255, 255, 255))
        self.screen.blit(title_text, (self.rect.x + self.PADDING, self.rect.y + 10))

        # Draw instruction
        instruction = self.small_font.render("Select the letter to be produced by the generator:", True, (180, 180, 180))
        self.screen.blit(instruction, (self.rect.x + self.PADDING, self.rect.y + 50))

        # Draw buttons
        for btn in self.letter_buttons:
            btn.draw(self.screen)