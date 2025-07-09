import pygame
import random

from machines.machine import Machine
from entities.item import Item
from core.port import Port, Direction

class Generator(Machine):
    def __init__(self, machine_data, rotation=0):
        self.image = machine_data.image
        self.size = machine_data.size
        self.rotation = rotation
        self.produced_letter=None

        self.production_interval = 2.0  # seconds between productions
        self.time_since_last_production = 0.0

        super().__init__(size=self.size, image=self.image, rotation=rotation)
    
    def init_ports(self):
        """Initialize ports for the generator"""
        # Add output port at center of top edge (relative to 3x3 machine)
        output_port = Port(
            relative_x=1,  # Center of 3x3 machine
            relative_y=0,  # Top edge
            direction=Direction.NORTH,
            port_type="output"
        )
        self.add_port(output_port)


    def produce_item(self):
        """Produce an item and try to output it"""
        if self.produced_letter is None:
            return None
        
        # Create item at the output port position
        if self.output_ports:
            output_port = self.output_ports[0]
            port_world_x, port_world_y = output_port.get_world_position()
            
            # Create item at port position
            item = Item(
                formula=self.produced_letter, 
                is_theorem=False, 
                position=(port_world_x * 32 + 16, port_world_y * 32 + 16)  # Center of tile
            )
            
            # Try to output the item
            if output_port.try_output_item(item):
                return item
        
        return None
    

    def change_letter(self, new_letter):
        """ Change the letter produced by the generator and update the image accordingly. """
        self.produced_letter = new_letter
        """ this does not work currently.
        font = pygame.font.SysFont(None, 34)
        text_surface = font.render(self.produced_letter, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2+13))
        self.image = pygame.image.load("assets/sprites/generator.png").convert_alpha()  # Reload the base image
        self.image.blit(text_surface, text_rect)"""

    
    def update(self, dt):
        """Call this every frame with dt = time elapsed since last call in seconds."""
        if self.produced_letter is None:
            return None

        self.time_since_last_production += dt

        if self.time_since_last_production >= self.production_interval:
            self.time_since_last_production -= self.production_interval
            return self.produce_item()

        return None