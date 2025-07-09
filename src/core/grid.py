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

        # Update connections for all machines after placing a new block
        self.update_all_connections()
    

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
        
        # Update connections for all machines after removing a block
        self.update_all_connections()


    def update_all_connections(self):
        """Update port connections for all machines in the grid"""
        for block in self.blocks.values(): # later: chunk system
            if hasattr(block, 'check_conveyor_connections'):
                block.check_conveyor_connections(self)


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
                result = block.update(dt)
                if result:
                    # For now, if it's an item that couldn't be placed, store it
                    # This is a fallback - normally items should go directly to conveyors
                    if hasattr(result, 'formula'):  # It's an item
                        self.items.append(result)
        
        # Update item movement and handle conveyor logic
        self.update_conveyor_system(dt)
    

    def update_conveyor_system(self, dt):
        """Update the conveyor system to move items between belts"""
        # Get all conveyor belts
        conveyors = [block for block in self.blocks.values() if hasattr(block, 'try_accept_item')]
        
        # Move items that are ready to transfer
        for conveyor in conveyors:
            if hasattr(conveyor, 'item_progress') and conveyor.item_progress >= 1.0:
                item = conveyor.try_output_item()
                if item:
                    # Try to pass item to next conveyor or machine
                    target_pos = conveyor.get_output_position()
                    target_block = self.get_block(target_pos[0], target_pos[1])
                    
                    if target_block and hasattr(target_block, 'try_accept_item'):
                        # It's another conveyor
                        if not target_block.try_accept_item(item):
                            # Target is full, put item back
                            conveyor.item = item
                            conveyor.item_progress = 1.0
                    else:
                        # No target or target doesn't accept items
                        # For now, remove item (later we can add logic for machines)
                        pass


    def draw_blocks(self, screen, camera):
        # TODO: only draw blocks, that are visible on the screen
        for (tile_x, tile_y), block in self.blocks.items():
            block.draw(screen, camera, tile_x, tile_y)

        for item in self.items:
            item.draw(screen, camera)

