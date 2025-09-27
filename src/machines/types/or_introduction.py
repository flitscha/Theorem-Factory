from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class OrIntroduction(LogicMachine):
    """
    Or-Introduction machine (3x3).
    - Two inputs: left-top (index 0), left-bottom (index 1), both West-facing.
    - One output: right-middle, East-facing.
    Rule: It must never be that both inputs contain plain formulas (is_theorem == False).
          If one input already contains a formula, the other input only accepts THEOREMS.
    Produces: BinaryOp('+', left.formula, right.formula) with is_theorem = True
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)
        self.input_roles = ["left", "right"]

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))


    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        # don't accept while there's an output waiting
        if self.output_item:
            return False

        index = self.ports.index(port)

        # if slot already occupied, reject
        if self.input_items[index]:
            return False

        other_index = 1 - index
        other = self.input_items[other_index]

        if other is None:
            # first item: accept anything (theorem or formula)
            self.input_items[index] = item
            return True
        else:
            # second item: enforce "at least one theorem" rule
            # if the other is a plain formula and this item is also a plain formula => reject
            if (not other.is_theorem) and (not item.is_theorem):
                return False

            # otherwise accept and start processing timer
            self.input_items[index] = item
            self.timer = 0.0
            return True


    def _process_items(self) -> Item:
        left = self.input_items[0]
        right = self.input_items[1]

        output_formula = BinaryOp("+", left.formula, right.formula)
        assumptions = set()
        if left.assumptions:
            assumptions.update(left.assumptions)
        if right.assumptions:
            assumptions.update(right.assumptions)

        return Item(
            formula=output_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )
