from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import Not
from machines.base.logic_machine import LogicMachine


class DoubleNotElimination(LogicMachine):
    """
    Double-Not-Elimination — 3x3 machine with single input and single output.
    - Input (west, middle) must be a THEOREM whose formula is --A.
    - The Output is A
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=1, rotation=rotation)

    def init_ports(self):
        self.add_port(Port(0, 1, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))

    # IReceiver: accept input item
    def receive_item_at_port(self, item, port):
        # don't accept while there's an output waiting to be taken, or the input is already occupied
        if self.output_item or self.input_items[0]:
            return False

        # strict acceptance rule:
        # - must be a theorem
        # - must be Not(Not(...)))
        if not item.is_theorem:
            return False

        if not isinstance(item.formula, Not) or not isinstance(item.formula.inner, Not):
            return False

        # accept
        self.input_items[0] = item
        self.timer = 0.0
        return True


    def _process_items(self):
        # extract conjunct
        item = self.input_items[0]
        inner_formula = item.formula.inner.inner
        assumptions = item.assumptions

        # produce the inner formula as theorem
        return Item(
            formula=inner_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )
    
