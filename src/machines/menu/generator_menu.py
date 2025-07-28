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
        self._create_letter_buttons()
    

    def _create_letter_buttons(self):
        """Create 26 letter buttons, and set the one currently selected."""
        margin = 10
        btn_width = 40
        btn_height = 40
        cols = 9

        # Calculate grid positioning
        grid_width = cols * btn_width + (cols - 1) * margin
        start_x = self.rect.centerx - grid_width // 2
        start_y = self.rect.y + 90

        self.letter_buttons.clear()

        # Create buttons
        for i, letter in enumerate(string.ascii_lowercase):
            x = start_x + (i % cols) * (btn_width + margin)
            y = start_y + (i // cols) * (btn_height + margin)

            # Create callback that handles single-selection logic
            callback = self._create_letter_callback(letter)

            selected = (letter == self.generator.produced_letter)
            btn = Button(
                rect=(x, y, btn_width, btn_height), 
                text=letter, 
                callback=callback, 
                font=self.font, 
                selected=selected
            )
            self.letter_buttons.append(btn)
    
    def _create_letter_callback(self, letter):
        """Create callback function for letter button"""
        def callback():
            self.set_letter(letter)
        return callback

    def set_letter(self, letter):
        """Set the generator's produced letter and update button states"""
        self.generator.produced_letter = letter
        self._update_button_selection()

    def _update_button_selection(self):
        """Update button selection states - only one can be selected"""
        for btn in self.letter_buttons:
            btn.set_selected(btn.text == self.generator.produced_letter)
    
    def update(self):
        """Update menu state - must be called every frame"""
        super().update()
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.letter_buttons:
            btn.update(mouse_pos)

    def handle_events(self, events):
        """Handle input events"""
        super().handle_events(events)
        for btn in self.letter_buttons:
            btn.handle_events(events)

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