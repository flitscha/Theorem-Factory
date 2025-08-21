from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import Not, Constant
from machines.base.logic_machine import LogicMachine


class FalseIntroduction(LogicMachine):
    """
    False-Introduction machine.
    Rule: If we have a theorem and the same theorem with "not" applied, the output is False.
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 1, Direction.EAST, "output"))

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if not item.is_theorem or self.output_item:
            return False
        
        index = self.ports.index(port)
        
        # if the port already has an item, dont accept
        if self.input_items[index]:
            return False

        # if both inputs are empty, always accept the item
        if self.input_items[0] is None and self.input_items[1] is None:
            self.input_items[index] = item
            return True

        # if the other input is already there, check if the new item fits together
        other_index = 0 if index == 1 else 1
        other_item = self.input_items[other_index]
        if other_item:
            # case 1: new_item is (not old_item)
            if isinstance(item.formula, Not) and item.formula.inner == other_item.formula:
                self.input_items[index] = item
                return True
            # case 2: (not new_item) is old_item
            elif isinstance(other_item.formula, Not) and other_item.formula.inner == item.formula:
                self.input_items[index] = item
                return True
        return False
    
    
    def _process_items(self) -> Item:
        assumptions0 = self.input_items[0].assumptions
        assumptions1 = self.input_items[1].assumptions
        output_assumptions = assumptions0 | assumptions1 # union

        return Item(
            formula=Constant(False),
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=output_assumptions
        )