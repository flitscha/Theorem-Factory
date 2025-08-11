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
        self.variable_buttons = [] # variables 'a' - 'z', excluding 't' and 'f'
        self.constant_buttons = [] # constants 'T' and 'F'
        self.t_mode_buttons = [] # 'T' can be a formula, of a theorem
        self._create_variable_buttons()
        self._create_constant_buttons()
    

    def _create_variable_buttons(self):
        """Create 24 variable buttons, using the letters 'a' to 'z', excluding 't' and 'f'."""
        margin = 10
        btn_width = 40
        btn_height = 40
        cols = 9

        # Calculate grid positioning
        grid_letters = [c for c in string.ascii_lowercase if c not in ('t', 'f')]
        grid_width = cols * btn_width + (cols - 1) * margin
        start_x = self.rect.centerx - grid_width // 2
        start_y = self.rect.y + 90

        self.variable_buttons.clear()

        # Create buttons
        for i, letter in enumerate(grid_letters):
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
            self.variable_buttons.append(btn)
    
    def _create_letter_callback(self, letter):
        """Create callback function for letter button"""
        def callback():
            self.set_letter(letter)
        return callback


    def _create_constant_buttons(self):
        # Create constants area (T and F) centered below the grid

        # same settings, as in _create_variable_buttons. (not ideal, same code twice)
        margin = 10
        btn_width = 40
        btn_height = 40
        cols = 9

        # Calculate grid positioning
        grid_letters = [c for c in string.ascii_lowercase if c not in ('t', 'f')]
        grid_width = cols * btn_width + (cols - 1) * margin
        start_x = self.rect.centerx - grid_width // 2
        start_y = self.rect.y + 90

        self.constant_buttons.clear()
        self.t_mode_buttons.clear()

        rows_used = (len(grid_letters) - 1) // cols + 1
        const_y = start_y + rows_used * (btn_height + margin) + 30
        const_btn_width = 60
        const_btn_height = 40
        total_const_width = 2 * const_btn_width + margin
        const_start_x = self.rect.centerx - total_const_width // 2

        # T button (special: has mode Formula / Theorem)
        t_callback = self._create_constant_callback('T')
        t_selected = (self.generator.produced_constant == 'T')
        t_btn = Button(
            rect=(const_start_x, const_y, const_btn_width, const_btn_height),
            text='T',
            callback=t_callback,
            font=self.font,
            selected=t_selected
        )
        self.constant_buttons.append(t_btn)

        # F button
        f_callback = self._create_constant_callback('F')
        f_selected = (self.generator.produced_constant == 'F')
        f_btn = Button(
            rect=(const_start_x + const_btn_width + margin, const_y, const_btn_width, const_btn_height),
            text='F',
            callback=f_callback,
            font=self.font,
            selected=f_selected
        )
        self.constant_buttons.append(f_btn)

        # T-mode buttons (Formula / Theorem) — small buttons, show only visually when T is selected
        toggle_width = 80
        toggle_height = 26
        toggle_x = const_start_x
        toggle_y = const_y + const_btn_height + 8

        formula_btn = Button(
            rect=(toggle_x, toggle_y, toggle_width, toggle_height),
            text='Formula',
            callback=lambda: self.set_constant('T', as_theorem=False),
            font=self.small_font,
            selected=(self.generator.produced_constant == 'T' and not self.generator.produced_is_theorem)
        )
        theorem_btn = Button(
            rect=(toggle_x + toggle_width + 8, toggle_y, toggle_width, toggle_height),
            text='Theorem',
            callback=lambda: self.set_constant('T', as_theorem=True),
            font=self.small_font,
            selected=(self.generator.produced_constant == 'T' and self.generator.produced_is_theorem)
        )
        self.t_mode_buttons = [formula_btn, theorem_btn]

    def _create_constant_callback(self, const_char):
        def callback():
            # default: T as Formula unless previously set to Theorem
            if const_char == 'T':
                # if T was already selected, keep its is_theorem flag; otherwise default False
                as_th = bool(self.generator.produced_is_theorem) if self.generator.produced_constant == 'T' else False
                self.set_constant('T', as_theorem=as_th)
            else:
                self.set_constant('F', as_theorem=False)
        return callback
    
    def set_letter(self, letter):
        """Set the generator's produced letter and update button states"""
        self.generator.produced_letter = letter
        self.generator.produced_constant = None
        self._update_button_selection()

    def set_constant(self, const_char, as_theorem=False):
        """Set generator to produce a constant ('T' or 'F'), for T optionally as theorem"""
        self.generator.change_constant(const_char, as_theorem=as_theorem)
        self._update_button_selection()

    def _update_button_selection(self):
        """Update selection state for all buttons"""
        for btn in self.variable_buttons:
            btn.set_selected(btn.text == self.generator.produced_letter)
        
        # constants selection
        for btn in self.constant_buttons:
            btn.set_selected(btn.text == (self.generator.produced_constant or ""))

        # T-mode buttons selection
        if self.generator.produced_constant == 'T':
            self.t_mode_buttons[0].set_selected(not self.generator.produced_is_theorem)  # Formula
            self.t_mode_buttons[1].set_selected(self.generator.produced_is_theorem)      # Theorem
        else:
            # deselect both if T not active
            for tb in self.t_mode_buttons:
                tb.set_selected(False)
    
    def update(self):
        """Update menu state - must be called every frame"""
        super().update()
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.variable_buttons + self.constant_buttons + self.t_mode_buttons:
            btn.update(mouse_pos)

    def handle_events(self, events):
        """Handle input events"""
        super().handle_events(events)
        for btn in self.variable_buttons + self.constant_buttons + self.t_mode_buttons:
            btn.handle_events(events)

    def draw(self):
        super().draw()

        # Draw heading
        title_text = self.font.render("Generator Settings", True, (255, 255, 255))
        self.screen.blit(title_text, (self.rect.x + self.PADDING, self.rect.y + 10))

        # Short instruction text
        instruction = self.small_font.render("Select the letter (variables) or a constant (T/F):", True, (180, 180, 180))
        self.screen.blit(instruction, (self.rect.x + self.PADDING, self.rect.y + 50))

        # Draw buttons
        for btn in self.variable_buttons:
            btn.draw(self.screen)
        
        # Draw constants label
        const_label = self.small_font.render("Constants:", True, (200, 200, 200))
        # position label above the constant buttons
        if self.constant_buttons:
            label_x = self.constant_buttons[0].rect.x
            label_y = self.constant_buttons[0].rect.y - 24
            self.screen.blit(const_label, (label_x, label_y))

        # Draw constant buttons (T and F)
        for btn in self.constant_buttons:
            btn.draw(self.screen)

        # If T is selected, draw the small mode buttons
        if self.generator.produced_constant == 'T':
            for btn in self.t_mode_buttons:
                btn.draw(self.screen)