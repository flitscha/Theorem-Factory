import pygame

from settings import *


class Grid():
    def __init__(self):
        # Dictionary to hold block objects {(x, y): block_object}
        # x and y are the world coordinates of the block (not screen coordinates)
        # x and y are snapped to the world grid
        self.blocks = {}

    def screen_to_world(self, screen_x, screen_y, camera_offset_x, camera_offset_y):
        """Convert screen coordinates to world coordinates based on camera offset."""
        # TODO: Implement zoom functionality
        world_x = (screen_x + camera_offset_x)
        world_y = (screen_y + camera_offset_y)
        return world_x, world_y

    def snap_to_grid(self, world_x, world_y):
        """Snap world coordinates to the grid."""
        snapped_x = (world_x // TILE_SIZE) * TILE_SIZE
        snapped_y = (world_y // TILE_SIZE) * TILE_SIZE
        return snapped_x, snapped_y
    

    def add_block(self, grid_x, grid_y, block):
        """Add a block to the grid at position (grid_x, grid_y).
        grid_x and grid_y are the snapped world coordinates."""
        self.blocks[(grid_x, grid_y)] = block
    
    def remove_block(self, grid_x, grid_y):
        """Remove the block from the grid at position (grid_x, grid_y), if it exists."""
        if (grid_x, grid_y) in self.blocks:
            del self.blocks[(grid_x, grid_y)]
    
    def get_block(self, grid_x, grid_y):
        """Get the block at position (x, y). Returns None if no block exists."""
        return self.blocks.get((grid_x, grid_y), None)
    

    def draw_grid_lines(self, screen, camera_offset_x, camera_offset_y):
        screen_width, screen_height = screen.get_size()
        start_x = -camera_offset_x % TILE_SIZE
        start_y = -camera_offset_y % TILE_SIZE

        # vertical lines
        x = start_x
        while x < screen_width:
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
            x += TILE_SIZE

        # horizontal lines
        y = start_y
        while y < screen_height:
            pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))
            y += TILE_SIZE

