import pygame
from config.settings import *

class InputProcessor:
    """Processes input events and translates them to game actions"""
    
    def __init__(self, input_handler, placement_preview, machine_selection_bar, machine_manager, game_state):
        self.input_handler = input_handler
        self.placement_preview = placement_preview
        self.machine_selection_bar = machine_selection_bar
        self.machine_manager = machine_manager
        self.game_state = game_state
        
    def process_input(self, screen):
        """Process all input and execute corresponding actions"""
        # Handle quit
        if self.input_handler.should_quit():
            return {"quit": True}
            
        # Handle rotation
        if self.input_handler.was_key_pressed(pygame.K_r):
            self.placement_preview.rotate_preview()
            
        # Handle left mouse click
        if self.input_handler.was_mouse_pressed(1):
            mouse_pos = self.input_handler.get_mouse_press_pos(1)
            self._handle_left_click(mouse_pos, screen)
            
        # Handle middle mouse click (remove machine)
        if self.input_handler.was_mouse_pressed(2):
            self.machine_manager.remove_machine_at_mouse()
            
        return {}
        
    def _handle_left_click(self, mouse_pos, screen):
        """Handle left mouse click based on current game state"""
        if self.game_state.is_menu_open():
            # Forward event to active menu
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": mouse_pos})
            self.game_state.active_menu.handle_event(event)
            
            if self.game_state.active_menu.closed:
                self.game_state.close_menu()
        else:
            # Handle machine selection from GUI
            selected = self.machine_selection_bar.handle_click(mouse_pos)
            
            if selected != "MISS":
                self.placement_preview.start_preview(selected)
            else:
                # Try to place machine or open menu
                if not self.machine_manager.try_place_machine(mouse_pos):
                    menu = self.machine_manager.create_menu_for_machine_at_mouse(screen)
                    if menu:
                        self.game_state.open_menu(menu)