import pygame
from .abstract_tool import AbstractTool

class PlacementTool(AbstractTool):
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

            # place machines
            if self.placement_preview.active_preview:
                s = self.machine_manager.try_place_machine(mouse_pos)
                # when the left mouse button is held, keep placing, if the current placement was either succesful,
                # or if the current position is occupied. (state s=0 or s=1)
                self.is_placing = (s == 0 or s == 1)


    def update(self, input_handler):
        # hold left mouse button for placing
        if self.is_placing and input_handler.is_key_held("mouse_1"):
            self.machine_manager.try_place_machine(pygame.mouse.get_pos())
        else:
            self.is_placing = False

