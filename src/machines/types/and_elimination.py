from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import BinaryOp


class AndElimination(Machine, IUpdatable, IReceiver, IProvider):
    """
    And-Elimination (∧E) — 3x3 machine with single input and single output.
    - Input (west, middle) must be a THEOREM whose formula is A * B.
    - In the machine menu the player chooses which conjunct to output (left or right).
    - Output is the chosen conjunct, and is a THEOREM (is_theorem=True).
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        # single input slot
        self.input_item = None
        self.input_offset = 0.0

        # processing
        self.timer = 0.0
        self.processing_duration = 3

        # single output slot (stashed until taken)
        self.output_item = None

        # 0 = left, 1 = right (default left)
        self.selected_side = 0

    def init_ports(self):
        input_port = Port(
            relative_x=0,
            relative_y=1,
            direction=Direction.WEST,
            port_type="input"
        )
        output_port = Port(
            relative_x=2,
            relative_y=1,
            direction=Direction.EAST,
            port_type="output"
        )
        self.add_port(input_port)
        self.add_port(output_port)

    # menu / external control
    def set_output_side(self, side):
        """side can be 0/1 or 'left'/'right'"""
        if side in (0, 'left'):
            self.selected_side = 0
        elif side in (1, 'right'):
            self.selected_side = 1
        else:
            raise ValueError("set_output_side expects 0/1 or 'left'/'right'")

    def get_output_side(self):
        return 'left' if self.selected_side == 0 else 'right'

    # IReceiver: accept input item
    def receive_item_at_port(self, item, port):
        # don't accept while there's an output waiting to be taken, or the input is already occupied
        if self.output_item or self.input_item:
            return False

        # strict acceptance rule:
        # - must be a theorem
        # - must be BinaryOp with operator '*'
        if not item.is_theorem:
            return False

        if not isinstance(item.formula, BinaryOp):
            return False

        if item.formula.op is not "*":
            return False

        # accept
        self.input_item = item
        self.timer = 0.0
        return True

    # IProvider: provide produced item
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.output_item = None
            return item
        return None

    def handle_backpressure(self, item, port):
        # stash produced item if downstream refuses
        if self.output_item is None:
            self.output_item = item
            self.timer = self.processing_duration
        else:
            print("Warning: (handle_backpressure) AND-ELIM already has an output item, ignoring new item.")

    def update(self, dt):
        # slide-in animation for the input item
        if self.input_item and self.input_offset < TILE_SIZE:
            self._move_item(self.input_item)
            self.input_offset += 0.5

        # process if we have an input
        if self.input_item:
            self.timer += dt
            if self.timer >= self.processing_duration:
                # extract conjunct
                binop = self.input_item.formula
                left = binop.left
                right = binop.right
                chosen = left if self.selected_side == 0 else right

                # produce chosen conjunct as theorem
                self.output_item = Item(
                    formula=chosen,
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    )
                )

                # clear input
                self.input_item = None
                self.input_offset = 0.0
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
        # draw contained input item
        if self.input_item:
            self.input_item.draw(screen, camera)
        super().draw(screen, camera)
