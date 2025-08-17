from machines.base.machine import Machine
from entities.item import Item
from entities.port import Port, Direction
from grid.interfaces import IUpdatable, IReceiver, IProvider
from config.constants import TILE_SIZE
from core.formula import Formula, BinaryOp


class OrElimination(Machine, IUpdatable, IReceiver, IProvider):
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
        super().__init__(machine_data, rotation=rotation)
        self.or_item = None # item "A or B"
        self.input_items = [None, None] # items "C" with assumptions "A" and "B" respectively

        # offsets for slide-in-animations
        self.or_offset = 0.0
        self.input_offsets = [0.0, 0.0]

        self.timer = 0.0
        self.processing_duration = 3.0
        self.output_item = None

    def init_ports(self):
        input1_port = Port(
            relative_x=0,
            relative_y=0,
            direction=Direction.WEST,
            port_type="input"
        )
        input2_port = Port(
            relative_x=0,
            relative_y=4,
            direction=Direction.WEST,
            port_type="input"
        )
        or_input_port = Port(
            relative_x=0,
            relative_y=2,
            direction=Direction.WEST,
            port_type="input"
        )
        output_port = Port(
            relative_x=2,
            relative_y=2,
            direction=Direction.EAST,
            port_type="output"
        )

        self.add_port(input1_port)
        self.add_port(input2_port)
        self.add_port(or_input_port)
        self.add_port(output_port)

    # IReceiver: Accept items 
    def receive_item_at_port(self, item, port):
        if self.output_item:
            return False

        # accept the or-input, if the item is an or-theorem
        if port == self.ports[2]:
            if self.or_item is None and item.is_theorem and isinstance(item.formula, BinaryOp) and item.formula.op == '+':
                self.or_item = item
                return True
            else:
                return False
        
        # only accept the other 2 inputs, if the or-theorem is already there
        if not self.or_item:
            return False
        
        left = self.or_item.formula.left
        right = self.or_item.formula.right

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
        

    # IProvider implementation
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.output_item = None
            return item
        else:
            return None

    def handle_backpressure(self, item, port):
        if self.output_item is None:
            self.output_item = item
            self.timer = self.processing_duration
        else:
            print("Warning: (handle_backpressure) OR-ELIMINATION already has an output item, ignoring new item.")


    def update(self, dt):
        # slide-in animation for items that are entering
        # first handle the 2 input theorems
        for i in range(2):
            if self.input_items[i] and self.input_offsets[i] < TILE_SIZE:
                self._move_item(self.input_items[i])
                self.input_offsets[i] += 0.5

        # handle the or-theorem
        if self.or_item and self.or_offset < TILE_SIZE:
            self._move_item(self.or_item)
            self.or_offset += 0.5

        # processing: only when all inputs present
        if self.or_item and self.input_items[0] and self.input_items[1]:
            self.timer += dt
            if self.timer >= self.processing_duration:
                
                # the output-formula is just one of the input_formulas
                output_formula = self.input_items[0].formula

                # calculate the assumptions
                left_formula = self.or_item.formula.left
                right_formula = self.or_item.formula.right

                or_assumptions = self.or_item.assumptions

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
                self.output_item = Item(
                    formula=output_formula,
                    is_theorem=True,
                    position=(
                        self.origin[0] * TILE_SIZE + TILE_SIZE,
                        self.origin[1] * TILE_SIZE + TILE_SIZE
                    ),
                    assumptions=output_assumptions
                )

                # reset the inputs and timer
                self.input_items = [None, None]
                self.or_item = None
                self.input_offsets = [0.0, 0.0]
                self.or_offset = 0.0
                self.timer = 0.0


    def _move_item(self, item):
        move_speed = 0.5
        if self.rotation == 0:
            item.position.x += move_speed
        elif self.rotation == 1:
            item.position.y += move_speed
        elif self.rotation == 2:
            item.position.x -= move_speed
        else:
            item.position.y -= move_speed


    def draw(self, screen, camera):
        # draw items
        for item in self.input_items:
            if item:
                item.draw(screen, camera)
        if self.or_item:
            self.or_item.draw(screen, camera)

        # draw machine sprite
        super().draw(screen, camera)
