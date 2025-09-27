from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import Not
from machines.base.logic_machine import LogicMachine

class Negator(LogicMachine):
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=1, rotation=rotation)
        #self.processing_item = None # item without the negation
        self.input_roles = ["input"]

    def init_ports(self):
        """Initialize 1 input (left) and 1 output (right)"""
        self.add_port(Port(0, 1, Direction.WEST, "input"))
        self.add_port(Port(1, 0, Direction.EAST, "output"))

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if item.is_theorem or self.input_items[0] or self.output_item:
            return False

        # Start processing this formula
        self.input_items[0] = item
        self.timer = 0.0
        return True


    def _process_items(self) -> Item:
        # Processing complete: create negated formula
        output_formula = Not(self.input_items[0].formula)
        return Item(
            formula=output_formula,
            is_theorem=False,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE, 
                self.origin[1] * TILE_SIZE + TILE_SIZE
            )
        )