import pygame
from config.constants import *
from game.game_state import *

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
        
    def process_input(self, screen, events, pause_menu):
        """Process all input and execute corresponding actions"""
        # Handle quit
        if self.input_handler.should_quit():
            return {"quit": True}
        
        # check if the pause-menu was closed. (Maybe it would be better, to allow the menu itself to change the state)
        if self.game_state.current_state == GameState.PAUSED and not pause_menu.is_open:
            self.game_state.resume_game()
        
        # Handle ESC key for pause menu
        if self.input_handler.was_key_pressed(pygame.K_ESCAPE):
            # close machine menus
            if self.game_state.is_menu_open():
                self.game_state.close_menu()
            
            # close pause-menu
            elif pause_menu.is_open and pause_menu.active_submenu is None:
                self.game_state.resume_game()
            
            elif not pause_menu.is_open:
                self.game_state.pause_game()
                pause_menu.open()

            
        
        # dont process game inputs, if paused
        if self.game_state.is_paused():
            return {}
        
        # Handle machine menu input
        if self.game_state.is_menu_open():
            self.game_state.active_menu.handle_events(events)
            if self.game_state.active_menu.closed:
                self.game_state.close_menu()
            return {}
        
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
        """Handle left mouse click for game interactions (not in machine-menu)"""
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
        """Open a machine menu (small menu for individual machines)"""
        menu = self.machine_manager.create_menu_for_machine_at_mouse(screen)
        if menu:
            self.game_state.open_menu(menu)