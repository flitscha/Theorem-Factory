from typing import Dict, List, Tuple, Optional
from machines.base.machine import Machine
from entities.port import Direction

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
        
        # disconnect ports
        block.disconnect_all_ports()

        # Remove from blocks dict
        origin_x, origin_y = block.origin
        del self.blocks[(origin_x, origin_y)]
        
        # Remove from occupied tiles
        for x in range(origin_x, origin_x + block.size[0]):
            for y in range(origin_y, origin_y + block.size[1]):
                del self.occupied_tiles[(x, y)]
        return block
    
    def get_block(self, grid_x: int, grid_y: int) -> Optional[Machine]:
        """Get block at position"""
        return self.occupied_tiles.get((grid_x, grid_y))
    
    def get_blocks_at_area(self, grid_x: int, grid_y: int, size: Tuple[int, int]) -> Dict[Tuple[int, int], Machine]:
        """Get all blocks in a specified area"""
        blocks = {}
        for x in range(grid_x, grid_x + size[0]):
            for y in range(grid_y, grid_y + size[1]):
                block = self.get_block(x, y)
                if block:
                    blocks[(x, y)] = block
        return blocks
    
    def is_empty(self, grid_x: int, grid_y: int, size: Tuple[int, int] = (1, 1)) -> bool:
        """Check if area is empty"""
        for x in range(grid_x, grid_x + size[0]):
            for y in range(grid_y, grid_y + size[1]):
                if self.occupied_tiles.get((x, y)):
                    return False
        return True
    
    def get_neighboring_machines(self, grid_x: int, grid_y: int) -> Dict[Direction, Optional[Machine]]:
        """Get neighboring machines around a position"""
        neighboring_machines = {}
        
        for direction in Direction:
            dx, dy = direction.as_vector()
            neighbor_pos = (grid_x + dx, grid_y + dy)
            machine = self.get_block(*neighbor_pos)
            if machine:
                neighboring_machines[direction] = machine
            else:
                neighboring_machines[direction] = None
        
        return neighboring_machines
    

    def get_neighboring_machines_of(self, machine: Machine) -> Dict[Direction, set[Machine]]:
        """Get all neighboring machines around the perimeter of a machine (no diagonals)."""
        if not machine:
            return {}
        
        origin_x, origin_y = machine.origin
        size_x, size_y = machine.size

        # initialize the dict
        neighbors: Dict[Direction, set[Machine]] = {d: set() for d in Direction}

        for x in range(origin_x, origin_x + size_x):
            # north
            top_neighbor = self.get_block(x, origin_y - 1)
            if top_neighbor:
                neighbors[Direction.NORTH].add(top_neighbor)

            # south
            bottom_neighbor = self.get_block(x, origin_y + size_y)
            if bottom_neighbor:
                neighbors[Direction.SOUTH].add(bottom_neighbor)

        for y in range(origin_y, origin_y + size_y):
            # west
            left_neighbor = self.get_block(origin_x - 1, y)
            if left_neighbor:
                neighbors[Direction.WEST].add(left_neighbor)

            # east
            right_neighbor = self.get_block(origin_x + size_x, y)
            if right_neighbor:
                neighbors[Direction.EAST].add(right_neighbor)

        return neighbors
    

    # save the machines of the grid to a json file
    def to_data(self) -> dict:
        return {
            "machines": [
                machine.to_data()
                for machine in self.blocks.values()
            ]
        }
