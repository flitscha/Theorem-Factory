import pygame
from .abstract_tool import AbstractTool

class EraserTool(AbstractTool):
    def __init__(self, machine_manager, placement_preview, machine_selection_bar, game_state):
        super().__init__(machine_manager, placement_preview, machine_selection_bar, game_state)
        self.is_deleting = False

    def handle_events(self, events, input_handler, screen):
        # left click
        if input_handler.was_mouse_pressed(1):
            # delete machine
            self.machine_manager.remove_machine_at_mouse()
            self.is_deleting = True

    def update(self, input_handler):
        # hold left mouse button for deleting
        if self.is_deleting and input_handler.is_key_held("mouse_1"):
            self.machine_manager.remove_machine_at_mouse()
        else:
            self.is_deleting = False
