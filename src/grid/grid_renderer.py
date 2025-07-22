import pygame
from config.settings import TILE_SIZE, GRID_LINE_COLOR
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt

class GridRenderer:
    """Handles rendering of the grid and its contents"""
    
    def __init__(self, grid_manager):
        self.grid_manager = grid_manager
    
    def draw_grid_lines(self, screen, camera):
        """Draw the grid lines"""
        screen_width, screen_height = screen.get_size()
        start_x = int(-(camera.offset_x % TILE_SIZE) * camera.zoom)
        start_y = int(-(camera.offset_y % TILE_SIZE) * camera.zoom)
        
        # Vertical lines
        x = start_x
        while x < screen_width:
            pygame.draw.line(screen, GRID_LINE_COLOR, (int(x), 0), (int(x), screen_height))
            x += TILE_SIZE * camera.zoom
        
        # Horizontal lines
        y = start_y
        while y < screen_height:
            pygame.draw.line(screen, GRID_LINE_COLOR, (0, int(y)), (screen_width, int(y)))
            y += TILE_SIZE * camera.zoom
    
    def _block_is_visible(self, block, camera) -> bool:
        """Check if the block is within the visible bounds of the camera"""
        min_x, max_x, min_y, max_y = camera.get_visible_tile_bounds()
        tile_x, tile_y = block.origin
        w, h = block.size
        
        return not (tile_x + w < min_x or tile_x > max_x or tile_y + h < min_y or tile_y > max_y)

    def draw_blocks(self, screen, camera):
        """Draw all blocks on the grid"""
        for (tile_x, tile_y), block in self.grid_manager.blocks.items():
            # Check if block is within visible bounds
            if not self._block_is_visible(block, camera):
                continue

            # Draw the block
            block.draw(screen, camera, tile_x, tile_y)
        
    
    def draw_items(self, screen, camera):
        """Draw all items on the grid"""
        for block in self.grid_manager.blocks.values():
            # Check if block is within visible bounds
            if not self._block_is_visible(block, camera):
                continue
            
            # Draw items on the conveyor belt
            if isinstance(block, ConveyorBelt):
                if block.item:
                    block.item.draw(screen, camera)
    