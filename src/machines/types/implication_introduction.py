from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from core.formula import Formula


class ImplicationIntroduction(Machine, IUpdatable, IReceiver, IProvider):
    """
    Implication-Introduction machine.
    Rule: If the conclusion contains the premise-formula in its assumptions, 
    this assumption gets removed in the resulting implication-theorem.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.premise_item = None
        self.conclusion_item = None
        # offsets for slide-in-animations
        self.premise_offset = 0.0
        self.conclusion_offset = 0.0

        self.timer = 0.0
        self.processing_duration = 3.0
        self.output_item = None

    def init_ports(self):
        premise_input_port = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        conclusion_input_port = Port(
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

        self.add_port(premise_input_port)
        self.add_port(conclusion_input_port)
        self.add_port(output_port)

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # premise input
            if self.premise_item is None and not item.is_theorem:
                self.premise_item = item
                return True
            else:
                return False
        elif port == self.ports[1]: # conclusion input
            if self.conclusion_item is None and item.is_theorem:
                self.conclusion_item = item
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
            print("Warning: (handle_backpressure) IMPLY-INTRO already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for items that are entering
        if self.premise_item and self.premise_offset < TILE_SIZE:
            self._move_item(self.premise_item)
            self.premise_offset += 0.5
        if self.conclusion_item and self.conclusion_offset < TILE_SIZE:
            self._move_item(self.conclusion_item)
            self.conclusion_offset += 0.5

        # processing: only when both inputs present
        if self.premise_item and self.conclusion_item:
            self.timer += dt
            if self.timer >= self.processing_duration:
                premise = self.premise_item.formula
                conclusion = self.conclusion_item.formula
                assumptions = self.conclusion_item.assumptions

                if premise in assumptions:
                    assumptions.remove(premise)

                output_formula = BinaryOp("->", premise, conclusion)

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
                self.conclusion_item = None
                self.premise_offset = 0.0
                self.conclusion_offset = 0.0
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
        if self.premise_item:
            self.premise_item.draw(screen, camera)
        if self.conclusion_item:
            self.conclusion_item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
