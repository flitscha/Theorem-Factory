from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.item import Item
    from machines.machine import Machine

class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

class Port:
    def __init__(self, relative_x: int, relative_y: int, direction: Direction, port_type: str):
        """
        relative_x, relative_y: Position relative to machine origin
        direction: Direction the port faces (where items go IN or OUT)
        port_type: "input" or "output"
        """
        self.relative_x = relative_x
        self.relative_y = relative_y
        self.direction = direction
        self.port_type = port_type
        self.machine = None  # Will be set when port is added to machine
        self.connected_conveyor = None  # Reference to connected conveyor belt
    
    def get_world_position(self) -> tuple:
        """Get the world grid position of this port"""
        if not self.machine or not self.machine.origin:
            return (0, 0)
        
        origin_x, origin_y = self.machine.origin
        return (origin_x + self.relative_x, origin_y + self.relative_y)
    
    def get_connection_position(self) -> tuple:
        """Get the grid position where a conveyor should connect to this port"""
        world_x, world_y = self.get_world_position()
        dx, dy = self.direction.value
        return (world_x + dx, world_y + dy)
    
    def can_accept_item(self) -> bool:
        """Check if this input port can accept an item"""
        return self.port_type == "input" and self.connected_conveyor is not None
    
    def can_output_item(self) -> bool:
        """Check if this output port can output an item"""
        return self.port_type == "output" and self.connected_conveyor is not None
    
    def try_output_item(self, item: 'Item') -> bool:
        """Try to output an item to connected conveyor"""
        if self.can_output_item():
            return self.connected_conveyor.try_accept_item(item)
        return False
    
    def try_input_item(self) -> Optional['Item']:
        """Try to get an item from connected conveyor"""
        if self.can_accept_item():
            return self.connected_conveyor.try_output_item()
        return None