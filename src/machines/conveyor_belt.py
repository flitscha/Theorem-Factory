import pygame
from typing import Optional
from machines.machine import Machine
from entities.item import Item
from core.port import Direction

class ConveyorBelt(Machine):
    def __init__(self, machine_data, rotation=0):
        super().__init__(size=(1, 1), image=machine_data.image, rotation=rotation)
        
        self.speed = 1.0  # tiles per second
        self.item = None  # Current item on this belt. (only one item at a time)
        self.item_progress = 0.0  # 0.0 to 1.0, how far item has traveled
        
        # Direction mapping based on rotation
        self.direction = self.get_direction_from_rotation(rotation)
        
        # Calculate input and output positions
        self.input_direction = self.get_opposite_direction(self.direction)
        self.output_direction = self.direction
    
    def get_direction_from_rotation(self, rotation):
        """Convert rotation (0,1,2,3) to Direction enum"""
        directions = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        return directions[rotation % 4]
    
    def get_opposite_direction(self, direction):
        """Get opposite direction"""
        opposite_map = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
        return opposite_map[direction]
    
    def get_input_position(self):
        """Get grid position where items enter this belt"""
        if not self.origin:
            return (0, 0)
        
        dx, dy = self.input_direction.value
        return (self.origin[0] + dx, self.origin[1] + dy)
    
    def get_output_position(self):
        """Get grid position where items exit this belt"""
        if not self.origin:
            return (0, 0)
        
        dx, dy = self.output_direction.value
        return (self.origin[0] + dx, self.origin[1] + dy)
    
    def try_accept_item(self, item: Item) -> bool:
        """Try to accept an item from input side"""
        if self.item is None:
            self.item = item
            self.item_progress = 0.0
            return True
        return False
    
    def try_output_item(self) -> Optional[Item]:
        """Try to output item to next belt/machine"""
        if self.item and self.item_progress >= 1.0:
            item = self.item
            self.item = None
            self.item_progress = 0.0
            return item
        return None
    
    def update(self, dt):
        """Update belt and item movement"""
        if self.item:
            self.item_progress += self.speed * dt
            self.item_progress = min(1.0, self.item_progress)
            
            # Update item visual position
            if self.origin:
                start_x = self.origin[0] * 32 + 16  # Center of tile
                start_y = self.origin[1] * 32 + 16
                
                dx, dy = self.direction.value
                target_x = start_x + dx * 32
                target_y = start_y + dy * 32
                
                # Interpolate position
                current_x = start_x + (target_x - start_x) * self.item_progress
                current_y = start_y + (target_y - start_y) * self.item_progress
                
                self.item.position.x = current_x
                self.item.position.y = current_y
    
    def draw(self, screen, camera, grid_x, grid_y):
        """Draw the conveyor belt"""
        super().draw(screen, camera, grid_x, grid_y) 