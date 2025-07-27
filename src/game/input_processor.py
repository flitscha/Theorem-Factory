import pygame
from config.settings import *

class InputProcessor:
    """Processes input events and translates them to game actions"""
    
    def __init__(self, input_handler, placement_preview, machine_selection_bar, machine_manager, game_state):
        # systems
        self.input_handler = input_handler
        self.placement_preview = placement_preview
        self.machine_selection_bar = machine_selection_bar
        self.machine_manager = machine_manager
        self.game_state = game_state

        # helper variables
        self.is_placing = False # True when placing a machine.
        # this is used to prevent placing machines, when lmb is held down, but the click started in a menu
        
    def process_input(self, screen):
        """Process all input and execute corresponding actions"""
        # Handle quit
        if self.input_handler.should_quit():
            return {"quit": True}
            
        # Handle rotation
        if self.input_handler.was_key_pressed(pygame.K_r):
            # if you are about to place a machine, rotate the preview
            if self.placement_preview.active_preview:
                self.placement_preview.rotate_preview()
            else:
                # otherwise, an existing machine should get rotated
                self.machine_manager.rotate_machine_at_mouse()
            
        # Handle left mouse click
        if self.input_handler.was_mouse_pressed(1):
            mouse_pos = self.input_handler.get_mouse_press_pos(1)
            self._handle_left_click(mouse_pos, screen)
            
        # Handle middle mouse click (remove machine)
        if self.input_handler.was_mouse_pressed(2):
            self.machine_manager.remove_machine_at_mouse()
        
        # handle behavior, when left mouse button is held down
        if self.is_placing and self.input_handler.is_key_held('mouse_1'):
            self.machine_manager.try_place_machine(pygame.mouse.get_pos())
        else:
            self.is_placing = False

            
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
            if mouse_pos[1] > SCREEN_HEIGHT - MACHINE_SELECTION_GUI_HEIGHT:
                selected = self.machine_selection_bar.handle_click(mouse_pos)
                if selected != "MISS":
                    self.placement_preview.start_preview(selected)
            else:
                # Try to place machine or open menu
                if self.placement_preview.active_preview:
                    # If a preview is active, try to place it
                    self.machine_manager.try_place_machine(mouse_pos)
                    self.is_placing = True
                else:
                    # If no preview, check if we clicked on a machine
                    self._open_machine_menu(mouse_pos, screen)
               

    def _open_machine_menu(self, mouse_pos, screen):
        menu = self.machine_manager.create_menu_for_machine_at_mouse(screen)
        if menu:
            self.game_state.open_menu(menu)
    