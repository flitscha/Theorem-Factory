from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from machines.base.logic_machine import LogicMachine


class Assumption(LogicMachine):
    """
    Assumption machine.
    - One input: left-middle, West-facing, for the formula.
    - One output: right-middle, East-facing, for the assumption formula.
    Rule: The input must be a formula, not a theorem, and the formula must not have an assumption.
    Produces: The same formula, but marked as an assumption.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=1, rotation=rotation)
        self.processing_duration = 1.5
        self.input_roles = ["formula"]

    def init_ports(self):
        self.add_port(Port(0, 1, Direction.WEST, "input"))
        self.add_port(Port(1, 1, Direction.EAST, "output"))

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item or self.input_items[0]:
            return False

        if not item.is_theorem: # input should be a formula
            self.input_items[0] = item
            self.timer = 0.0
            return True
        else:
            return False


    def _process_items(self) -> Item:
        formula = self.input_items[0].formula
        output_formula = formula

        return Item(
            formula=output_formula,
            is_theorem=True, # The output is a theorem, because it's an assumption
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions={formula}
        )
