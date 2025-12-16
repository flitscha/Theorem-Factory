import pygame
from config.constants import *
from core.performance_tracker import performance_tracker

class Renderer:
    """Handles all rendering operations"""
    
    def __init__(self, screen):
        self.screen = screen
        
    def clear_screen(self, color=(0, 0, 0)):
        """Clear screen with specified color"""
        self.screen.fill(color)
        
    def render_game_world(self, grid, camera):
        """Render the main game world elements"""
        performance_tracker.start("render.grid")
        grid.draw_grid_lines(self.screen, camera)
        performance_tracker.end("render.grid")

        performance_tracker.start("render.belts")
        grid.draw_conveyor_belts(self.screen, camera)
        performance_tracker.end("render.belts")

        performance_tracker.start("render.items")
        grid.draw_items(self.screen, camera)
        performance_tracker.end("render.items")

        performance_tracker.start("render.machines")
        grid.draw_machines(self.screen, camera)
        performance_tracker.end("render.machines")
    
    def render_highlights(self, grid, camera, active_tool):
        """Render highlights. For example, before you delete a machine, the machine gets red"""
        grid.draw_highlight(self.screen, camera, active_tool)
        
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