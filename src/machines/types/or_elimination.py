from entities.item import Item
from entities.port import Port, Direction
from config.constants import TILE_SIZE
from core.formula import BinaryOp
from machines.base.logic_machine import LogicMachine


class OrElimination(LogicMachine):
    """
    Or-Elimination machine.
    Inputs: 
        A theorem of the form "A or B"
        A theorem C with A in its assumptions
        The same theorem C with B in its assumptions
    Output:
        The Theorem C, with appropriate assumptions
    """
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, num_inputs=3, rotation=rotation)
        # input_items[0]: theorem C with assumption A
        # input_items[1]: theorem C with assumption B
        # input_items[2]: theorem A or B
        self.input_roles = ["theorem-from-A", "theorem-from-B", "A-or-B"]
        

    def init_ports(self):
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 4, Direction.WEST, "input"))
        self.add_port(Port(0, 2, Direction.WEST, "input"))
        self.add_port(Port(2, 2, Direction.EAST, "output"))


    # IReceiver: Accept items 
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        # accept the or-input, if the item is an or-theorem
        if port == self.ports[2]:
            if self.input_items[2] is None and item.is_theorem and isinstance(item.formula, BinaryOp) and item.formula.op == '+':
                self.input_items[2] = item
                return True
            else:
                return False
        
        # only accept the other 2 inputs, if the or-theorem is already there
        if not self.input_items[2]:
            return False
        
        left = self.input_items[2].formula.left
        right = self.input_items[2].formula.right

        index = self.ports.index(port) # 0 or 1
        other_index = 0 if index == 1 else 1
        other_item = self.input_items[other_index]

        # if the input is already full, dont accept the item
        if self.input_items[index]:
            return False
        
        # if the other item is already there: check if the assumptions are correct
        if other_item:
            # the formula has to be the same
            if item.formula != other_item.formula:
                return False
            
            # and we have to check the assumptions
            if left in other_item.assumptions and right in item.assumptions:
                self.input_items[index] = item
                return True
            elif right in other_item.assumptions and left in item.assumptions:
                self.input_items[index] = item
                return True
            else:
                return False
        # if both inputs are empty, we are more flexible.
        else:
            if left in item.assumptions or right in item.assumptions:
                self.input_items[index] = item
                return True
            else:
                return False
        
    def _process_items(self) -> Item:
        # the output-formula is just one of the input_formulas
        output_formula = self.input_items[0].formula

        # calculate the assumptions
        left_formula = self.input_items[2].formula.left
        right_formula = self.input_items[2].formula.right

        or_assumptions = self.input_items[2].assumptions

        assumptions0 = self.input_items[0].assumptions
        assumptions1 = self.input_items[1].assumptions

        # remove some assumptions
        if left_formula in assumptions0 and right_formula in assumptions1:
            assumptions0.remove(left_formula)
            assumptions1.remove(right_formula)
        elif right_formula in assumptions0 and left_formula in assumptions1:
            assumptions0.remove(right_formula)
            assumptions1.remove(left_formula)
        else:
            print("ERROR in or_elimination: Wrong assumptions in the inputs. Should not happen. This should be avoided by receive_item_at_port()")

        output_assumptions = or_assumptions | assumptions0 | assumptions1

        # create the output item
        return Item(
            formula=output_formula,
            is_theorem=True,
            position=(
                self.origin[0] * TILE_SIZE + TILE_SIZE,
                self.origin[1] * TILE_SIZE + TILE_SIZE
            ),
            assumptions=output_assumptions
        )

