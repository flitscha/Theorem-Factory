from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import Not, Constant


class NotIntroduction(Machine, IUpdatable, IReceiver, IProvider):
    """
    Not-Introduction machine.
    Rule: If we have the theorem "F" (False) with some assumptions, and one of its assumptions,
    the output will be "not" this assumption.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.false_item = None
        self.assumption_item = None
        self.output_item = None

        self.timer = 0.0
        self.processing_duration = 3.0
        self.false_offset = 0.0
        self.assumption_offset = 0.0

    def init_ports(self):
        false_input_port = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        assumption_input_port = Port(
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

        self.add_port(false_input_port)
        self.add_port(assumption_input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # assumption input
            if self.assumption_item is None and self.false_item and item.formula in self.false_item.assumptions:
                self.assumption_item = item
                return True
            else:
                return False
            
        elif port == self.ports[1]: # false input
            if self.false_item is None and item.is_theorem and isinstance(item.formula, Constant) and item.formula.value == False:
                self.false_item = item
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
            print("Warning: (handle_backpressure) NOT-INTRO already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for items that are entering
        if self.false_item and self.false_offset < TILE_SIZE:
            self._move_item(self.false_item)
            self.false_offset += 0.5
        if self.assumption_item and self.assumption_offset < TILE_SIZE:
            self._move_item(self.assumption_item)
            self.assumption_offset += 0.5

        if self.false_item and self.assumption_item and not self.output_item:
            self.timer += dt
            if self.timer >= self.processing_duration:
                false_item = self.false_item
                assumption_item = self.assumption_item

                assumption = assumption_item.formula
                assumptions = set(false_item.assumptions)
                assumptions.remove(assumption)

                output_formula = Not(assumption)

                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ),
                    assumptions=assumptions
                )

                self.false_item = None
                self.assumption_item = None
                self.false_offset = 0.0
                self.assumption_offset = 0.0
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
        if self.false_item:
            self.false_item.draw(screen, camera)
        if self.assumption_item:
            self.assumption_item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
