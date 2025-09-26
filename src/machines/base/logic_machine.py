from grid.interfaces import IProvider, IReceiver, IUpdatable
from machines.base.machine import Machine
from config.constants import TILE_SIZE
from entities.item import Item


class LogicMachine(Machine, IUpdatable, IReceiver, IProvider):
    """
    Base class for the natural-deduction machines.
    A lot is the same for all machines, so this class provides the common functionality.
    """
    def __init__(self, machine_data, num_inputs=0, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        
        self.input_items = [None] * num_inputs
        self.input_offsets = [0.0] * num_inputs
        self.input_roles = ["input"] * num_inputs # e.g. for Implication-Elimination: ["implication", "premise"]
        self.output_item = None
        self.last_output_item = None
        self.timer = 0.0
        self.processing_duration = 3.0

    # slide-in animation for input items
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
    

    def _reset_inputs(self):
        for i in range(len(self.input_items)):
            self.input_items[i] = None
            self.input_offsets[i] = 0.0
        self.timer = 0.0

    
    def update(self, dt):
        # slide-in animation for input items
        for i, item in enumerate(self.input_items):
            if item and self.input_offsets[i] < TILE_SIZE:
                self._move_item(item)
                self.input_offsets[i] += 0.5

        # start processing if ready
        if self._ready_to_process():
            self.timer += dt
            if self.timer >= self.processing_duration:
                self.output_item = self._process_items()
                # reset
                self._reset_inputs()

    # IProvider implementation
    def provide_item_from_port(self, port):
        if self.output_item:
            item = self.output_item
            self.last_output_item = self.output_item
            self.output_item = None
            return item
        return None

    def handle_backpressure(self, item, port):
        if self.output_item is None:
            self.output_item = item
            #self.timer = self.processing_duration # problems: it could happen, that the timer jumps from 0 to 3 instantly
        else:
            print(f"Warning: {self.__class__.__name__} already has an output item, ignoring new item.")

    def draw(self, screen, camera):
        for item in self.input_items:
            if item:
                item.draw(screen, camera)
        super().draw(screen, camera)

    # functions that each specific machine must implement
    def _ready_to_process(self) -> bool:
        for item in self.input_items:
            if item is None:
                return False
        return True

    def _process_items(self) -> Item:
        raise NotImplementedError

    
