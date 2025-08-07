from enum import Enum
from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE

class BinaryConnectiveType(Enum):
    AND = "*"
    OR = "+"
    IMPLIES = "->"

    def apply(self, a: str, b: str) -> str:
        return f"({a} {self.value} {b})"
    
class BinaryConnective(Machine, IUpdatable, IReceiver, IProvider):
    # binary connectives: or, and, implication
    # the player can select one of the connectives in a machine-menu
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.selected_connective = BinaryConnectiveType.AND
        self.input_items = [None, None] # two inputs
        self.input_offsets = [0.0, 0.0] # keep track, how far an item moved into the machine
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
            relative_x=1,
            relative_y=1,
            direction=Direction.EAST,
            port_type="output"
        )
        self.add_port(input_port_top)
        self.add_port(input_port_bottom)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if item.is_theorem or self.output_item: #or not self.selected_connective:
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

    # IProvider: Provide output
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
            print("Warning: (handle_backpressure) AND already has an item, ignoring new item.")
            pass


    
    def update(self, dt):
        # slide-in animation
        for i in range(2):
            if self.input_items[i] and self.input_offsets[i] < TILE_SIZE:
                self._move_item(self.input_items[i])
                self.input_offsets[i] += 0.5

        # timer runs, if both items are in
        if self.input_items[0] and self.input_items[1]:
            self.timer += dt
            if self.timer >= self.processing_duration:
                new_formula = self.selected_connective.apply(
                    self.input_items[0].formula, self.input_items[1].formula
                )
                self.output_item = Item(
                    formula=new_formula,
                    is_theorem=False,
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
        # draw items
        for i, item in enumerate(self.input_items):
            if item:
                item.draw(screen, camera)

        # draw the machine
        super().draw(screen, camera)