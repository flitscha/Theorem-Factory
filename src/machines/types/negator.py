from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import Not

class Negator(Machine, IUpdatable, IReceiver, IProvider):
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.processing_item = None # item without the negation
        self.timer = 0.0 # Time elapsed during processing
        self.processing_duration = 3.0
        self.output_item = None # Item ready to be output (with negation)

    def init_ports(self):
        """Initialize 1 input (left) and 1 output (right)"""
        input_port = Port(
            relative_x=0,
            relative_y=1,
            direction=Direction.WEST,
            port_type="input"
        )
        output_port = Port(
            relative_x=1,
            relative_y=0,
            direction=Direction.EAST,
            port_type="output"
        )
        self.add_port(input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if item.is_theorem or self.processing_item or self.output_item:
            return False

        # Start processing this formula
        self.processing_item = item
        self.timer = 0.0
        return True

    # IProvider: Provide output
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.output_item = None
            return item
        return None

    def handle_backpressure(self, item, port):
        # If output is blocked, keep it ready
        if self.output_item is None:
            self.output_item = item
            self.timer = self.processing_duration
        else:
            print("Warning: (handle_backpressure) negator already has an item, ignoring new item.")
            pass

    def update(self, dt):
        # If processing, count time
        if self.processing_item:
            self.timer += dt
            self._update_processing_item_position()
            if self.timer >= self.processing_duration:
                # Processing complete: create negated formula
                output_formula = Not(self.processing_item.formula)
                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=False,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE, 
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ) # item is not visible like this in the first frame
                )
                self.processing_item = None
                self.timer = 0.0
    

    def _update_processing_item_position(self):
        if self.timer > 1.0:
            return
        
        if self.rotation == 0:
            self.processing_item.position.x += 0.5
        elif self.rotation == 1:
            self.processing_item.position.y += 0.5
        elif self.rotation == 2:
            self.processing_item.position.x -= 0.5
        else:
            self.processing_item.position.y -= 0.5
    
    def draw(self, screen, camera):
        # draw item first
        if self.processing_item:
            self.processing_item.draw(screen, camera)

        # draw the machine over the item
        super().draw(screen, camera)
