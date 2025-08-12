from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE


class Assumption(Machine, IUpdatable, IReceiver, IProvider):
    """
    Assumption machine.
    - One input: left-middle, West-facing, for the formula.
    - One output: right-middle, East-facing, for the assumption formula.
    Rule: The input must be a formula, not a theorem, and the formula must not have an assumption.
    Produces: The same formula, but marked as an assumption.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.input_item = None
        self.timer = 0.0
        self.processing_duration = 1.5
        self.output_item = None

    def init_ports(self):
        input_port = Port(
            relative_x=0,
            relative_y=1,
            direction=Direction.WEST,
            port_type="input"
        )
        output_port = Port(
            relative_x=1,
            relative_y=1,
            direction=Direction.EAST,
            port_type="output"
        )

        self.add_port(input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if self.input_item is None:
            if not item.is_theorem: # input should be a formula
                self.input_item = item
                self.timer = 0.0
                return True
            else:
                return False
        else:
            return False

    # IProvider: Provide output to the right
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.output_item = None
            return item
        else:
            return None

    def handle_backpressure(self, item, port):
        if self.output_item is None:
            self.output_item = item
            self.timer = self.processing_duration
        else:
            print("Warning: (handle_backpressure) ASSUMPTION already has an item, ignoring new item.")
            pass


    def update(self, dt):
        # processing: only when input present
        if self.input_item:
            self._update_input_item_position()
            self.timer += dt
            if self.timer >= self.processing_duration:
                formula = self.input_item.formula
                output_formula = formula

                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=True, # The output is a theorem, because it's an assumption
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ),
                    assumptions={formula}
                )

                self.input_item = None
                self.timer = 0.0


    def _update_input_item_position(self):
        if self.timer > 1.0:
            return
        
        if self.rotation == 0:
            self.input_item.position.x += 0.5
        elif self.rotation == 1:
            self.input_item.position.y += 0.5
        elif self.rotation == 2:
            self.input_item.position.x -= 0.5
        else:
            self.input_item.position.y -= 0.5


    def draw(self, screen, camera):
        # draw items
        if self.input_item:
            self.input_item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
