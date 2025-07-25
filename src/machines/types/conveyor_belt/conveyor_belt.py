import pygame
from pygame.math import Vector2

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
        self.item_start_position = Vector2(0, 0) # tuple of (x, y) where the item starts on the belt
        self.item_end_position = Vector2(0, 0)

        # Define input and output directions
        # This can change, e.g. when the belt is a curve
        # There can be multiple inputs and outputs, if multiple adjacent belts are connected
        self.inputs = [] # does NOT change with rotation
        self.outputs = []

        # Round robin indices
        self.next_output_index = 0
        self.next_input_index = 0

        super().__init__(size=machine_data.size, image=machine_data.image, rotation=rotation)


    def init_ports(self):
        """Initialize ports based on inputs and outputs"""
        # Clear existing ports
        self.clear_ports()

        for direction in self.inputs:
            port = Port(0, 0, direction, "input")
            self.add_port(port)
        
        for direction in self.outputs:
            port = Port(0, 0, direction, "output")
            self.add_port(port)

    def update_sprite(self, sprite_path, horizontal_mirror=False, vertical_mirror=False):
        """Update the sprite based on inputs and outputs"""
        self.image = pygame.image.load(sprite_path).convert_alpha()
        if horizontal_mirror:
            self.image = pygame.transform.flip(self.image, True, False)
        if vertical_mirror:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rotate_image()


    # IProvider interface implementation
    def provide_item_from_port(self, port):
        """Nur der 'dran'-Port darf aktuell ein Item liefern (Round Robin)."""
        if not self.item or self.item_progress < 1.0:
            return None

        # Prüfen, ob dieser Port der aktuelle Output ist
        output_ports = self.output_ports
        if not output_ports:
            return None

        # Index normalisieren
        current_index = self.next_output_index % len(output_ports)
        if port != output_ports[current_index]:
            return None

        # Item abgeben und Index weiterschalten
        item = self.item
        self.item = None
        self.item_progress = 0.0
        self.next_output_index = (self.next_output_index + 1) % len(output_ports)
        return item


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
        """Nur der 'dran'-Input darf aktuell ein Item annehmen (Round Robin)."""
        if self.item is not None:
            return False

        input_ports = self.input_ports
        if not input_ports:
            return False

        # check if this port is the current input
        current_index = self.next_input_index % len(input_ports)
        if port != input_ports[current_index]:
            return False

        # accept the item
        self.item = item
        self.item_progress = 0.0
        # update the start and end position of the item. (used to interpolate the item position)
        self.item_start_position = self._get_start_position_of_item(input_index=current_index)
        self.item_end_position = self._get_end_position_of_item()
        self.next_input_index = (self.next_input_index + 1) % len(input_ports)
        return True


    # IUpdatable interface implementation
    def update(self, dt):
        """Update belt and item movement"""
        if self.item:
            self.item_progress += self.speed * dt
            self.item_progress = min(1.0, self.item_progress)
            
            # Update item visual position
            self._update_item_position()
    
    def _get_start_position_of_item(self, input_index):
        """Get the start position of the item on the belt"""
        input = self.inputs[input_index]
        previous_input_direction = input.rotate(self.rotation)
        target_x, target_y = self.origin[0] * 32 + 16, self.origin[1] * 32 + 16  # Center of this tile
        start_x = target_x + previous_input_direction.value[0] * 32
        start_y = target_y + previous_input_direction.value[1] * 32
        return Vector2(start_x, start_y)
    
    def _get_end_position_of_item(self):
        """Get the end position of the item on the belt"""
        return Vector2(self.origin[0] * 32 + 16, self.origin[1] * 32 + 16)

        
    def _update_item_position(self):
        """
        Update the visual position of the item on the belt
        The item starts at the center of the previous tile (the used input of this conveyor belt),
        and moves in this direction, until it reaches the center of this belt.
        """
        self.item.position = self.item_start_position.lerp(self.item_end_position, self.item_progress)

        
    def draw(self, screen, camera, grid_x, grid_y):
        """Draw the conveyor belt"""
        super().draw(screen, camera, grid_x, grid_y)