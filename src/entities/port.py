from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.item import Item
    from src.machines.base.machine import Machine

class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def as_vector(self): 
        return self.value

    @staticmethod    
    def from_rotation(rotation: int):
        """Convert rotation (0,1,2,3) to Direction enum"""
        directions = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        return directions[rotation % 4]
    
    def opposite(self):
        """Get the opposite direction"""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
        return opposites[self]
    
    def rotate(self, rotation: int):
        """Rotate this direction by the given rotation (0, 1, 2, 3)"""
        directions = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        index = (directions.index(self) + rotation) % 4
        return directions[index]

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
        self.port_type = port_type # "input" or "output"
        self.machine: Optional['Machine'] = None  # Set when added to a machine
        self.connected_port: Optional['Port'] = None  # Direct connection to another port
    
    def get_grid_position(self) -> tuple:
        """Get the world grid position of this port"""
        if not self.machine or not self.machine.origin:
            return (0, 0)
        
        origin_x, origin_y = self.machine.origin
        return (origin_x + self.relative_x, origin_y + self.relative_y)
    
    def get_connection_position(self) -> tuple:
        """Get the grid position where another port should connect to this port"""
        world_x, world_y = self.get_grid_position()
        dx, dy = self.direction.as_vector()
        return (world_x + dx, world_y + dy)
    
    def can_connect_to(self, other: 'Port') -> bool:
        """Returns True if this port can logically connect to the other."""
        if self.port_type == other.port_type:
            return False  # Only input ↔ output allowed
        if self.get_connection_position() != other.get_grid_position():
            return False  # Must face each other spatially
        if self.direction != other.direction.opposite():
            return False  # Must face each other directionally
        return True

    def connect_if_possible(self, other_machine: 'Machine') -> bool:
        """Try to connect this port to a compatible port on the other machine."""
        target_ports = (
            other_machine.input_ports if self.port_type == "output"
            else other_machine.output_ports
        )

        for other in target_ports:
            if self.can_connect_to(other):
                self.connected_port = other
                other.connected_port = self
                return True
        return False
    
    def is_connected(self) -> bool:
        return self.connected_port is not None

    def disconnect(self):
        if self.connected_port:
            self.connected_port.connected_port = None
            self.connected_port = None
    

    def try_output_item(self, item: 'Item') -> bool:
        """Try to send item to connected input port."""
        if self.port_type != "output" or not self.connected_port:
            return False
        return self.connected_port.receive_item(item)

    def try_input_item(self) -> Optional['Item']:
        """Try to get item from connected output port."""
        if self.port_type != "input" or not self.connected_port:
            return None
        return self.connected_port.provide_item()

    def receive_item(self, item: 'Item') -> bool:
        """Default receive behavior – pass to machine."""
        if self.port_type != "input":
            return False
        return self.machine.receive_item_at_port(self, item)

    def provide_item(self) -> Optional['Item']:
        """Default provide behavior – get from machine."""
        if self.port_type != "output":
            return None
        return self.machine.provide_item_from_port(self)