import pygame

from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IProvider
from core.utils import world_to_screen
from config.constants import TILE_SIZE, GENERATOR_LETTER_OFFSETS
from core.formula import Variable, Constant

class Generator(Machine, IUpdatable, IProvider):
    def __init__(self, machine_data, rotation=0):
        self.rotation = rotation
        self.produced_letter=None
        self.produced_constant = None  # 'T' or 'F'
        self.produced_is_theorem = False  # only meaningful when produced_constant == 'T'

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
        self.produced_constant = None
        self.produced_is_theorem = False
    
    def change_constant(self, const_char: str, as_theorem: bool = False):
        """
        Set generator to produce a constant 'T' or 'F'.
        If const_char == 'T' and as_theorem == True, produced items will be theorems.
        """
        if const_char not in ("T", "F"):
            raise ValueError("Only 'T' or 'F' are allowed as constants.")
        self.produced_constant = const_char
        self.produced_letter = None
        # only T can be a theorem in our UI; keep the flag but ignore for F
        self.produced_is_theorem = bool(as_theorem) if const_char == "T" else False


    # IProvider interface implementation
    def provide_item_from_port(self, port):
        if (self.produced_letter is None and self.produced_constant is None) or \
        self.time_since_last_production < self.production_interval:
            return None
    
        # Create item at the output port position
        port_world_x, port_world_y = port.get_grid_position()

        # create the formula and item
        if self.produced_constant == "T":
            formula = Constant(True)
            is_theorem = self.produced_is_theorem
        elif self.produced_constant == "F":
            formula = Constant(False)
            is_theorem = False
        else:
            formula = Variable(self.produced_letter)
            is_theorem = False

        item = Item(
            formula=formula, 
            is_theorem=is_theorem,
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
        super().draw(screen, camera)

        produced_text = None
        if self.produced_constant is not None:
            produced_text = self.produced_constant
        elif self.produced_letter:
            produced_text = self.produced_letter

        if produced_text:
            base_x, base_y = world_to_screen(self.origin[0] * TILE_SIZE, self.origin[1] * TILE_SIZE, camera)
            offset_x, offset_y = GENERATOR_LETTER_OFFSETS[self.rotation]

            letter_x = base_x + offset_x * camera.zoom
            letter_y = base_y + offset_y * camera.zoom

            # render letter
            zoomed_font_size = int(22 * camera.zoom)
            font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", zoomed_font_size)

            text_surface = font.render(produced_text, True, (15, 15, 15))
            text_rect = text_surface.get_rect(center=(letter_x, letter_y))

            screen.blit(text_surface, text_rect)

