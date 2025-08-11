from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import BinaryOp


class AndIntroduction(Machine, IUpdatable, IReceiver, IProvider):
    """
    And-Introduction machine (3x3).
    - Two inputs: left-top (index 0), left-bottom (index 1), both West-facing.
    - One output: right-middle, East-facing.
    Rule: Both inputs must be THEOREMS
    Produces: BinaryOp('*', left.formula, right.formula) with is_theorem = True
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.input_items = [None, None]  # two inputs (index 0 = top, 1 = bottom)
        self.input_offsets = [0.0, 0.0]
        self.timer = 0.0
        self.processing_duration = 3.0
        self.output_item = None

    def init_ports(self):
        input_port_top = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        input_port_bottom = Port(
            relative_x=0,
            relative_y=2,
            direction=Direction.WEST,
            port_type="input"
        )
        output_port = Port(
            relative_x=2,
            relative_y=1,
            direction=Direction.EAST,
            port_type="output"
        )

        self.add_port(input_port_top)
        self.add_port(input_port_bottom)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        # only accept theorems
        if not item.is_theorem or self.output_item:
            return False

        index = self.ports.index(port)
        if index == 0 and self.input_items[0] is None:
            self.input_items[0] = item
        elif index == 1 and self.input_items[1] is None:
            self.input_items[1] = item
        else:
            return False

        # if both inputs are ready, start timer
        if self.input_items[0] and self.input_items[1]:
            self.timer = 0.0

        return True
    

    # IProvider: Provide output to the right
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.output_item = None
            return item
        return None

    def handle_backpressure(self, item, port):
        if self.output_item is None:
            self.output_item = item
            self.timer = self.processing_duration
        else:
            print("Warning: (handle_backpressure) AND-INTRO already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for items that are entering
        for i in range(2):
            if self.input_items[i] and self.input_offsets[i] < TILE_SIZE:
                self._move_item(self.input_items[i])
                self.input_offsets[i] += 0.5

        # processing: only when both inputs present
        if self.input_items[0] and self.input_items[1]:
            self.timer += dt
            if self.timer >= self.processing_duration:
                left = self.input_items[0]
                right = self.input_items[1]

                output_formula = BinaryOp("*", left.formula, right.formula)

                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    )
                )

                self.input_items = [None, None]
                self.input_offsets = [0.0, 0.0]
                self.timer = 0.0

    def _move_item(self, item):
        move_speed = 0.5
        if self.rotation == 0:
            item.position.x += move_speed
        elif self.rotation == 1:
            item.position.y += move_speed
        elif self.rotation == 2:
            item.position.x -= move_speed
        else:
            item.position.y -= move_speed

    def draw(self, screen, camera):
        for item in self.input_items:
            if item:
                item.draw(screen, camera)

        super().draw(screen, camera)
