import pygame
from typing import Optional
from machines.base.machine import Machine
from entities.item import Item
from entities.port import Direction
from grid.interfaces import IUpdatable, IProvider, IReceiver
from entities.port import Port

class ConveyorBelt(Machine, IUpdatable, IProvider, IReceiver):
    def __init__(self, machine_data, rotation=0):
        
        self.speed = 1.0  # tiles per second
        self.item = None  # Current item on this belt. (only one item at a time)
        self.item_progress = 0.0  # 0.0 to 1.0, how far item has traveled

        super().__init__(size=machine_data.size, image=machine_data.image, rotation=rotation)

    def init_ports(self):
        # Initialize input and output ports based on direction        
        input_port = Port(0, 0, Direction.WEST, "input") # direction based on the base-sprite without rotation
        self.add_port(input_port)

        output_port = Port(0, 0, Direction.EAST, "output")
        self.add_port(output_port)
    

    # IProvider interface implementation  
    def provide_item_from_port(self, port): # simple: a conveyor belt only has one output port
        """Called when the output port is asked for an item"""
        if self.item and self.item_progress >= 1.0:
            item = self.item
            self.item = None
            self.item_progress = 0.0
            return item
        return None
    
    def handle_backpressure(self, item: Item, port: Port):
        """Handle backpressure when output is blocked"""
        # If output is blocked, we just keep the item on the belt
        # No special handling needed since we only allow one item at a time
        if self.item is None:
            self.item = item
            self.item_progress = 1.0 # idk if this is right. Because like this, the belt tries each frame to output the item 
            # Idea: notify the conveyor, when it is ready to output the item
        else:
            # If we already have an item, we can ignore the new one (should not happen normally)
            print("Warning: (handle_backpressure) Conveyor belt already has an item, ignoring new item.")
            pass
    

    # IReceiver interface implementation
    def receive_item_at_port(self, port: Port, item: Item) -> bool:
        """Called when the input port receives an item"""
        if self.item is None:
            self.item = item
            self.item_progress = 0.0
            return True
        return False
        

    # IUpdatable interface implementation
    def update(self, dt):
        """Update belt and item movement"""
        if self.item:
            self.item_progress += self.speed * dt
            self.item_progress = min(1.0, self.item_progress)
            
            # Update item visual position
            self._update_item_position()
        
    def _update_item_position(self):
        """Update the visual position of the item on the belt"""
        if not self.item or not self.origin:
            return
        
        # Calculate start and end positions
        start_x = self.origin[0] * 32 + 16  # Center of tile
        start_y = self.origin[1] * 32 + 16
        
        dx, dy = Direction.from_rotation(self.rotation).as_vector()
        target_x = start_x + dx * 32
        target_y = start_y + dy * 32
        
        # Interpolate position based on progress
        current_x = start_x + (target_x - start_x) * self.item_progress
        current_y = start_y + (target_y - start_y) * self.item_progress
        
        self.item.position.x = current_x
        self.item.position.y = current_y

        
    def draw(self, screen, camera, grid_x, grid_y):
        """Draw the conveyor belt"""
        super().draw(screen, camera, grid_x, grid_y)
        
        if self.item:
            self.item.draw(screen, camera)