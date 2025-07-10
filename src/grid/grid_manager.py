from typing import Dict, Tuple, Optional, Set
from machines.base.machine import Machine
from grid.interfaces import IUpdatable, IConveyorNode, IItemAcceptor, IItemProducer

class GridManager:
    """Manages the placement and removal of blocks on the grid"""
    
    def __init__(self):
        self.blocks: Dict[Tuple[int, int], Machine] = {}
        self.occupied_tiles: Dict[Tuple[int, int], Machine] = {}
        # Collections for different types of objects
        self.updatable_blocks: Set[Machine] = set()
        self.conveyor_nodes: Set[Machine] = set()
        self.item_acceptors: Set[Machine] = set()
        self.item_producers: Set[Machine] = set()
    
    def add_block(self, grid_x: int, grid_y: int, block: Machine):
        """Add a block to the grid"""
        block.origin = (grid_x, grid_y)
        self.blocks[(grid_x, grid_y)] = block
        
        # Add to occupied tiles
        for x in range(grid_x, grid_x + block.rotated_size[0]):
            for y in range(grid_y, grid_y + block.rotated_size[1]):
                self.occupied_tiles[(x, y)] = block
        
        # Register block in appropriate collections
        self._register_block_interfaces(block)
    
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
        
        # Unregister from collections
        self._unregister_block_interfaces(block)
        
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
    
    def _register_block_interfaces(self, block: Machine):
        """Register block in appropriate interface collections"""
        
        if isinstance(block, IUpdatable):
            self.updatable_blocks.add(block)
        if isinstance(block, IConveyorNode):
            self.conveyor_nodes.add(block)
        if isinstance(block, IItemAcceptor):
            self.item_acceptors.add(block)
        if isinstance(block, IItemProducer):
            self.item_producers.add(block)
    
    def _unregister_block_interfaces(self, block: Machine):
        """Unregister block from interface collections"""
        self.updatable_blocks.discard(block)
        self.conveyor_nodes.discard(block)
        self.item_acceptors.discard(block)
        self.item_producers.discard(block)