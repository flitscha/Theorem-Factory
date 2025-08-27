from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class ImplicationIntroduction(LogicMachine):
    """
    Implication-Introduction machine.
    Rule: If the conclusion contains the premise-formula in its assumptions, 
    this assumption gets removed in the resulting implication-theorem.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)
        # input_items[0]: premise (not a theorem)
        # input_items[1]: conclusion (a theorem)

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))


    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # premise input
            if self.input_items[0] is None and not item.is_theorem:
                self.input_items[0] = item
                return True
            else:
                return False
        elif port == self.ports[1]: # conclusion input
            if self.input_items[1] is None and item.is_theorem:
                self.input_items[1] = item
                return True
            else:
                return False
        else:
            return False

    def _process_items(self) -> Item:
        premise = self.input_items[0].formula
        conclusion = self.input_items[1].formula
        assumptions = self.input_items[1].assumptions

        if premise in assumptions:
            assumptions.remove(premise)

        output_formula = BinaryOp("->", premise, conclusion)

        return Item(
            formula=output_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )

