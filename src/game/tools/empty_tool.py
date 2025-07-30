import pygame
from game.tools.abstract_tool import AbstractTool

class EmptyTool(AbstractTool):
    def __init__(self, machine_manager, placement_preview, machine_selection_bar, game_state):
        super().__init__(machine_manager, placement_preview, machine_selection_bar, game_state)
        self.is_placing = False

    def handle_inputs(self, input_handler, screen):
        # Rotation
        if input_handler.was_key_pressed(pygame.K_r):
            if self.placement_preview.active_preview:
                self.placement_preview.rotate_preview()
            else:
                self.machine_manager.rotate_machine_at_mouse()

        # Left click
        if input_handler.was_mouse_pressed(1):
            mouse_pos = input_handler.get_mouse_press_pos(1)
            self._open_machine_menu(mouse_pos, screen)


    def _open_machine_menu(self, mouse_pos, screen):
        menu = self.machine_manager.create_menu_for_machine_at_mouse(screen)
        if menu:
            self.game_state.open_menu(menu)