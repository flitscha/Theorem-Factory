from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class ImplicationElimination(LogicMachine):
    """
    Implication-Elimination machine.
    Rule: If we have an implication A -> B and A, we can conclude B.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)
        self.input_roles = ["implication", "premise"]
        # input_item[0]: implication (A -> B)
        # input_item[1]: premise (A)
        # output_item: conclusion (B)


    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))


    # IReceiver: Accept items TODO: update
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # implication input
            if self.input_items[0] is None and item.is_theorem and isinstance(item.formula, BinaryOp) and item.formula.op == "->":
                self.input_items[0] = item
                return True
            else:
                return False
        elif port == self.ports[1]: # premise input
            # only proceed, when the implication is already there. This avoids unwanted inputs
            if self.input_items[1] is None and self.input_items[0] and self.input_items[0].formula.left == item.formula:
                self.input_items[1] = item
                return True
            else:
                return False
        else:
            return False


    def _process_items(self) -> Item:
        # get the assumptions for the output-formula
        implication_assumptions = self.input_items[0].assumptions
        premise_assumptions = self.input_items[1].assumptions
        assumptions = implication_assumptions | premise_assumptions # union

        # create the output
        output_formula = self.input_items[0].formula.right

        return Item(
            formula=output_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )
