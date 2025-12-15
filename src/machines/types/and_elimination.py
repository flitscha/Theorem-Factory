from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class AndElimination(LogicMachine):
    """
    And-Elimination (∧E) — 3x3 machine with single input and single output.
    - Input (west, middle) must be a THEOREM whose formula is A * B.
    - In the machine menu the player chooses which conjunct to output (left or right).
    - Output is the chosen conjunct, and is a THEOREM (is_theorem=True).
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=1, rotation=rotation)

        # 0 = left, 1 = right (default left)
        self.selected_side = 0
        self.input_roles = ["conjunction"]

    def init_ports(self):
        self.add_port(Port(0, 1, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))

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
        if self.output_item or self.input_items[0]:
            return False

        # strict acceptance rule:
        # - must be a theorem
        # - must be BinaryOp with operator '*'
        if not item.is_theorem:
            return False

        if not isinstance(item.formula, BinaryOp):
            return False

        if item.formula.op != "*":
            return False

        # accept
        self.input_items[0] = item
        self.timer = 0.0
        return True


    def _process_items(self):
        # extract conjunct
        item = self.input_items[0]
        binop = item.formula
        left = binop.left
        right = binop.right
        chosen = left if self.selected_side == 0 else right
        assumptions = item.assumptions

        # produce chosen conjunct as theorem
        return Item(
            formula=chosen,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )

    # save / load stuff
    def _add_custom_data(self, data: dict):
        data["selected_side"] = self.selected_side

    def _load_custom_data(self, data: dict):
        self.selected_side = data.get("selected_side", 0)