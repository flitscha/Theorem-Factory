from typing import Dict, Tuple, Optional
from machines.base.machine import Machine

class GridManager:
    """Manages the placement and removal of blocks on the grid"""
    
    def __init__(self):
        self.blocks: Dict[Tuple[int, int], Machine] = {}
        self.occupied_tiles: Dict[Tuple[int, int], Machine] = {}
    
    def add_block(self, grid_x: int, grid_y: int, block: Machine):
        """Add a block to the grid"""
        block.origin = (grid_x, grid_y)
        self.blocks[(grid_x, grid_y)] = block
        
        # Add to occupied tiles
        for x in range(grid_x, grid_x + block.size[0]):
            for y in range(grid_y, grid_y + block.size[1]):
                self.occupied_tiles[(x, y)] = block
        
    def remove_block(self, grid_x: int, grid_y: int) -> Optional[Machine]:
        """Remove block at position"""
        block = self.occupied_tiles.get((grid_x, grid_y))
        if not block:
            return None
        
        origin_x, origin_y = block.origin
        
        # Remove from blocks dict
        del self.blocks[(origin_x, origin_y)]
        
        # Remove from occupied tiles
        for x in range(origin_x, origin_x + block.rotated_size[0]):
            for y in range(origin_y, origin_y + block.rotated_size[1]):
                del self.occupied_tiles[(x, y)]
        return block
    
    def get_block(self, grid_x: int, grid_y: int) -> Optional[Machine]:
        """Get block at position"""
        return self.occupied_tiles.get((grid_x, grid_y))
    
    def is_empty(self, grid_x: int, grid_y: int, size: Tuple[int, int] = (1, 1)) -> bool:
        """Check if area is empty"""
        for x in range(grid_x, grid_x + size[0]):
            for y in range(grid_y, grid_y + size[1]):
                if self.occupied_tiles.get((x, y)):
                    return False
        return True