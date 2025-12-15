from enum import Enum
from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine

class BinaryConnectiveType(Enum):
    AND = "*"
    OR = "+"
    IMPLIES = "->"

    def apply(self, a: str, b: str) -> str:
        return f"({a} {self.value} {b})"
    
    def symbol(self):
        return self.value
    
class BinaryConnective(LogicMachine):
    # binary connectives: or, and, implication
    # the player can select one of the connectives in a machine-menu
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=2, rotation=rotation)
        self.selected_connective = BinaryConnectiveType.AND
        self.input_roles = ["left", "right"]

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(1, 1, Direction.EAST, "output"))

    # IReceiver: Accept items
    def receive_item_at_port(self, item, port):
        if item.is_theorem or self.output_item: #or not self.selected_connective:
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


    def _process_items(self) -> Item:
        output_formula = BinaryOp(
            self.selected_connective.symbol(), 
            self.input_items[0].formula, 
            self.input_items[1].formula
        )
        return Item(
            formula=output_formula,
            is_theorem=False,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            )
        )
    
    # save / load stuff
    def _add_custom_data(self, data: dict):
        data["selected_connective"] = self.selected_connective.name

    def _load_custom_data(self, data: dict):
        name = data.get("selected_connective", "AND")
        self.selected_connective = BinaryConnectiveType[name]