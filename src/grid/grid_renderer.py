import pygame
from config.settings import TILE_SIZE, GRID_COLOR

class GridRenderer:
    """Handles rendering of the grid and its contents"""
    
    def __init__(self, grid_manager):
        self.grid_manager = grid_manager
    
    def draw_grid_lines(self, screen, camera):
        """Draw the grid lines"""
        screen_width, screen_height = screen.get_size()
        start_x = -(camera.offset_x % TILE_SIZE) * camera.zoom
        start_y = -(camera.offset_y % TILE_SIZE) * camera.zoom
        
        # Vertical lines
        x = start_x
        while x < screen_width:
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
            x += TILE_SIZE * camera.zoom
        
        # Horizontal lines
        y = start_y
        while y < screen_height:
            pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))
            y += TILE_SIZE * camera.zoom
    
    def draw_blocks(self, screen, camera):
        """Draw all blocks on the grid"""
        for (tile_x, tile_y), block in self.grid_manager.blocks.items():
            # Check if block is within visible bounds
            min_x, max_x, min_y, max_y = camera.get_visible_tile_bounds()
            w, h = block.size
            if tile_x + w < min_x or tile_x > max_x:
                continue
            if tile_y + h < min_y or tile_y > max_y:
                continue

            block.draw(screen, camera, tile_x, tile_y)
    