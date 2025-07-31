import pygame

from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IProvider
from core.utils import world_to_screen
from config.constants import TILE_SIZE, GENERATOR_LETTER_OFFSETS

class Generator(Machine, IUpdatable, IProvider):
    def __init__(self, machine_data, rotation=0):
        self.rotation = rotation
        self.produced_letter=None

        self.production_interval = 2.0  # seconds between productions
        self.time_since_last_production = 0.0

        #self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", zoomed_font_size)

        super().__init__(machine_data, rotation=rotation)
    
    def init_ports(self):
        """Initialize ports for the generator"""
        # Add output port at center of top edge (relative to 3x3 machine)
        output_port = Port(
            relative_x=1,  # Center of 3x3 machine
            relative_y=2,  # Bottom edge
            direction=Direction.SOUTH,
            port_type="output"
        )
        self.add_port(output_port)

    def change_letter(self, new_letter):
        """ Change the letter produced by the generator and update the image accordingly. """
        self.produced_letter = new_letter


    # IProvider interface implementation
    def provide_item_from_port(self, port):
        if self.produced_letter is None or self.time_since_last_production < self.production_interval:
            return None
    
        # Create item at the output port position
        port_world_x, port_world_y = port.get_grid_position()
        item = Item(
            formula=self.produced_letter, 
            is_theorem=False,
            position=(port_world_x * 32 + 16, port_world_y * 32 + 16)
        )

        self.time_since_last_production = 0.0 # reset timer
        return item
    
    def handle_backpressure(self, item, port):
        """Handle backpressure when output is blocked"""
        # If output is blocked, we try to produce the item again later
        self.time_since_last_production = self.production_interval - 0.1


    # IUpdatable interface implementation
    def update(self, dt):
        """Call this every frame with dt = time elapsed since last call in seconds."""
        self.time_since_last_production += dt
    

    def draw(self, screen, camera):
        # Erst das normale Maschinenbild zeichnen
        super().draw(screen, camera)

        if self.produced_letter:
            base_x, base_y = world_to_screen(self.origin[0] * TILE_SIZE, self.origin[1] * TILE_SIZE, camera)

            """
            sprite_w = self.size[0] * TILE_SIZE
            sprite_h = self.size[1] * TILE_SIZE
            center_x = sprite_w / 2
            center_y = sprite_h / 2
            rel_offset_x = 49 - center_x
            rel_offset_y = 44 - center_y
            rot_x, rot_y = rotate_point(rel_offset_x, rel_offset_y, self.rotation)
            offset_x = center_x + rot_x
            offset_y = center_y + rot_y
            """
            offset_x, offset_y = GENERATOR_LETTER_OFFSETS[self.rotation]

            letter_x = base_x + offset_x * camera.zoom
            letter_y = base_y + offset_y * camera.zoom

            # render letter
            zoomed_font_size = int(22 * camera.zoom)
            font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", zoomed_font_size)

            text_surface = font.render(self.produced_letter, True, (15, 15, 15))
            text_rect = text_surface.get_rect(center=(letter_x, letter_y))

            screen.blit(text_surface, text_rect)

