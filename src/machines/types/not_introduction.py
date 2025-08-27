from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import Not, Constant
from machines.base.logic_machine import LogicMachine


class NotIntroduction(LogicMachine):
    """
    Not-Introduction machine.
    Rule: If we have the theorem "F" (False) with some assumptions, and one of its assumptions,
    the output will be "not" this assumption.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)
        # input_items[0]: False (theorem)
        # input_items[1]: assumption (to be negated)
        # output_item: Not(assumption)


    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))


    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        if port == self.ports[0]: # assumption input
            if self.input_items[1] is None and self.input_items[0] and item.formula in self.input_items[0].assumptions:
                self.input_items[1] = item
                return True
            else:
                return False
            
        elif port == self.ports[1]: # false input
            if self.input_items[0] is None and item.is_theorem and isinstance(item.formula, Constant) and item.formula.value == False:
                self.input_items[0] = item
                return True
            else:
                return False
        else:
            return False


    def _process_items(self) -> Item:
        assumption = self.input_items[1].formula
        assumptions = set(self.input_items[0].assumptions)
        assumptions.remove(assumption)

        output_formula = Not(assumption)

        return Item(
            formula=output_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=assumptions
        )