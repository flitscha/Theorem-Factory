from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from core.formula import Formula


class ImplicationElimination(Machine, IUpdatable, IReceiver, IProvider):
    """
    Implication-Elimination machine.
    Rule: If we have an implication A -> B and A, we can conclude B.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.implication_item = None
        self.premise_item = None
        self.output_item = None

        self.timer = 0.0
        self.processing_duration = 3.0
        self.implication_offset = 0.0
        self.premise_offset = 0.0

    def init_ports(self):
        implication_input_port = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        premise_input_port = Port(
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

        self.add_port(implication_input_port)
        self.add_port(premise_input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # implication input
            if self.implication_item is None and item.is_theorem and isinstance(item.formula, BinaryOp) and item.formula.op == "->":
                self.implication_item = item
                return True
            else:
                return False
        elif port == self.ports[1]: # premise input
            # only proceed, when the implication is already there. This avoids unwanted inputs
            if self.premise_item is None and self.implication_item and self.implication_item.formula.left == item.formula:
                self.premise_item = item
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
            print("Warning: (handle_backpressure) IMPLY-ELIM already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for items that are entering
        if self.implication_item and self.implication_offset < TILE_SIZE:
            self._move_item(self.implication_item)
            self.implication_offset += 0.5
        if self.premise_item and self.premise_offset < TILE_SIZE:
            self._move_item(self.premise_item)
            self.premise_offset += 0.5

        # processing the inputs
        if self.implication_item and self.premise_item and not self.output_item:
            self.timer += dt
            if self.timer >= self.processing_duration:
                # get the assumptions for the output-formula
                implication_assumptions = self.implication_item.assumptions
                premise_assumptions = self.premise_item.assumptions
                assumptions = implication_assumptions | premise_assumptions # union

                # create the output
                output_formula = self.implication_item.formula.left

                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ),
                    assumptions=assumptions
                )

                self.premise_item = None
                self.implication_item = None
                self.premise_offset = 0.0
                self.implication_offset = 0.0
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
        if self.implication_item:
            self.implication_item.draw(screen, camera)
        if self.premise_item:
            self.premise_item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
