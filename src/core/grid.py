import pygame

from config.settings import *


class Grid():
    def __init__(self):
        # Dictionary to hold block objects {(x, y): block_object}
        # x and y are the world coordinates of the block (not screen coordinates)
        # x and y are snapped to the world grid
        self.blocks = {}
        self.occupied_tiles = {} # Set to keep track of occupied tiles for quick lookup
        self.items = []


    def add_block(self, grid_x, grid_y, block):
        """Add a block to the grid at position (grid_x, grid_y).
        grid_x and grid_y are grid-koordinates. (distance 1, is TILE_SIZE in Woorld-coordinates)"""

        block.origin = (grid_x, grid_y)
        self.blocks[(grid_x, grid_y)] = block

        # Add the block to the occupied tiles set
        for x in range(grid_x, grid_x + block.rotated_size[0]):
            for y in range(grid_y, grid_y + block.rotated_size[1]):
                self.occupied_tiles[(x, y)] = block
    

    def remove_block(self, grid_x, grid_y):
        """Remove the block from the grid at position (grid_x, grid_y), if it exists."""
        block = self.occupied_tiles.get((grid_x, grid_y))
        if not block:
            return  # no block here
        
        origin_x, origin_y = block.origin

        # Remove from blocks dict
        del self.blocks[(origin_x, origin_y)]

        # Remove all occupied tiles of this block
        for x in range(origin_x, origin_x + block.rotated_size[0]):
            for y in range(origin_y, origin_y + block.rotated_size[1]):
                del self.occupied_tiles[(x, y)]


    def get_block(self, grid_x, grid_y):
        """Get the block at position (x, y). Returns None if no block exists."""
        return self.occupied_tiles.get((grid_x, grid_y))


    def is_empty(self, grid_x, grid_y, size=(1, 1)):
        """Check if the grid area defined by (grid_x, grid_y) and size is empty."""
        for x in range(grid_x, grid_x + size[0]):
            for y in range(grid_y, grid_y + size[1]):
                if self.occupied_tiles.get((x, y)):
                    return False
        return True
    

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


    def update(self, dt):
        # Iterate over all blocks and call their update method if it exists
        for block in self.blocks.values():
            if hasattr(block, "update"):
                item = block.update(dt) # TODO: improve. Where should items be stored? Only on convayor belt?
                if item:
                    self.items.append(item)


    def draw_blocks(self, screen, camera):
        # TODO: only draw blocks, that are visible on the screen
        for (tile_x, tile_y), block in self.blocks.items():
            block.draw(screen, camera, tile_x, tile_y)

        for item in self.items:
            item.draw(screen, camera)

