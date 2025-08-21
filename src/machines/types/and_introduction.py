from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class AndIntroduction(LogicMachine):
    """
    And-Introduction machine (3x3).
    - Two inputs: left-top (index 0), left-bottom (index 1), both West-facing.
    - One output: right-middle, East-facing.
    Rule: Both inputs must be THEOREMS
    Produces: BinaryOp('*', left.formula, right.formula) with is_theorem = True
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        # only accept theorems
        if not item.is_theorem or self.output_item:
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
    

    def _process_items(self):
        left, right = self.input_items
        formula = BinaryOp("*", left.formula, right.formula)
        assumptions = set()
        if left.assumptions:
            assumptions.update(left.assumptions)
        if right.assumptions:
            assumptions.update(right.assumptions)

        return Item(
            formula=formula,
            is_theorem=True,
            position=(self.origin[0]*TILE_SIZE+TILE_SIZE,
                      self.origin[1]*TILE_SIZE+TILE_SIZE),
            assumptions=assumptions
        )
    
