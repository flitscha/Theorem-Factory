import pygame

from settings import *


class Grid():
    def __init__(self):
        # Dictionary to hold block objects {(x, y): block_object}
        # x and y are the world coordinates of the block (not screen coordinates)
        # x and y are snapped to the world grid
        self.blocks = {}


    def add_block(self, grid_x, grid_y, block):
        """Add a block to the grid at position (grid_x, grid_y).
        grid_x and grid_y are grid-koordinates. (distance 1, is TILE_SIZE in Woorld-coordinates)"""
        self.blocks[(grid_x, grid_y)] = block
    
    def remove_block(self, grid_x, grid_y):
        """Remove the block from the grid at position (grid_x, grid_y), if it exists."""
        if (grid_x, grid_y) in self.blocks:
            del self.blocks[(grid_x, grid_y)]
    
    def get_block(self, grid_x, grid_y):
        """Get the block at position (x, y). Returns None if no block exists."""
        return self.blocks.get((grid_x, grid_y), None)
    

    def draw_grid_lines(self, screen, camera_offset_x, camera_offset_y, camera_zoom):
        screen_width, screen_height = screen.get_size()
        start_x = -(camera_offset_x % TILE_SIZE) * camera_zoom
        start_y = -(camera_offset_y % TILE_SIZE) * camera_zoom

        # vertical lines
        x = start_x
        while x < screen_width:
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
            x += TILE_SIZE * camera_zoom

        # horizontal lines
        y = start_y
        while y < screen_height:
            pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))
            y += TILE_SIZE * camera_zoom


    def draw_blocks(self, screen, camera):
        # TODO: only draw blocks, that are visible on the screen
        for (tile_x, tile_y), block in self.blocks.items():
            block.draw(screen, camera, tile_x, tile_y)

