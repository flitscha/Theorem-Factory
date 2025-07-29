import pygame
from config.constants import *

class Renderer:
    """Handles all rendering operations"""
    
    def __init__(self, screen):
        self.screen = screen
        
    def clear_screen(self, color=(0, 0, 0)):
        """Clear screen with specified color"""
        self.screen.fill(color)
        
    def render_game_world(self, grid, camera):
        """Render the main game world elements"""
        grid.draw_grid_lines(self.screen, camera)
        grid.draw_conveyor_belts(self.screen, camera)
        grid.draw_items(self.screen, camera)
        grid.draw_machines(self.screen, camera)
        
    def render_gui_components(self, components):
        """Render all GUI components"""
        for component in components:
            if hasattr(component, 'draw'):
                component.draw()
            
    def render_debug_info(self, debug, camera, clock):
        """Render debug information overlay"""
        debug.draw(self.screen, camera, clock)
        
    def present(self):
        """Present the final rendered frame"""
        pygame.display.flip()