from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IProvider

class Generator(Machine, IUpdatable, IProvider):
    def __init__(self, machine_data, rotation=0):
        self.rotation = rotation
        self.produced_letter=None

        self.production_interval = 2.0  # seconds between productions
        self.time_since_last_production = 0.0

        super().__init__(size=machine_data.size, image=machine_data.image, rotation=rotation)
    
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
        """ this does not work currently.
        font = pygame.font.SysFont(None, 34)
        text_surface = font.render(self.produced_letter, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.image.get_width()//2, self.image.get_height()//2+13))
        self.image = pygame.image.load("assets/sprites/generator.png").convert_alpha()  # Reload the base image
        self.image.blit(text_surface, text_rect)"""


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
