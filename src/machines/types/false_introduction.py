from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import Not, Constant


class FalseIntroduction(Machine, IUpdatable, IReceiver, IProvider):
    """
    False-Introduction machine.
    Rule: If we have a theorem and the same theorem with "not" applied, the output is False.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.input_items = [None, None]
        self.input_offsets = [0.0, 0.0]
        self.output_item = None

        self.timer = 0.0
        self.processing_duration = 3.0

    def init_ports(self):
        theorem_input_port = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        not_theorem_input_port = Port(
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

        self.add_port(theorem_input_port)
        self.add_port(not_theorem_input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if not item.is_theorem or self.output_item:
            return False
        
        index = self.ports.index(port)
        
        # if the port already has an item, dont accept
        if self.input_items[index]:
            return False

        # if both inputs are empty, always accept the item
        if self.input_items[0] is None and self.input_items[1] is None:
            self.input_items[index] = item
            return True

        # if the other input is already there, check if the new item fits together
        other_index = 0 if index == 1 else 1
        other_item = self.input_items[other_index]
        if other_item:
            # case 1: new_item is (not old_item)
            if isinstance(item.formula, Not) and item.formula.inner == other_item.formula:
                self.input_items[index] = item
                return True
            # case 2: (not new_item) is old_item
            elif isinstance(other_item.formula, Not) and other_item.formula.inner == item.formula:
                self.input_items[index] = item
                return True
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
            print("Warning: (handle_backpressure) FALSE-INTRO already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for items that are entering
        for i in range(2):
            if self.input_items[i] and self.input_offsets[i] < TILE_SIZE:
                self._move_item(self.input_items[i])
                self.input_offsets[i] += 0.5

        # processing: only when both inputs present
        if self.input_items[0] and self.input_items[1] and not self.output_item:
            self.timer += dt
            if self.timer >= self.processing_duration:
                assumptions0 = self.input_items[0].assumptions
                assumptions1 = self.input_items[1].assumptions
                output_assumptions = assumptions0 | assumptions1 # union

                self.output_item = Item(
                    formula=Constant(False),
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ),
                    assumptions=output_assumptions
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
        for item in self.input_items:
            if item:
                item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
