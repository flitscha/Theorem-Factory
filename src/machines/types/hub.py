from core.theorem_key import TheoremKey
from entities.item import Item
from entities.port import Port, Direction
from config.constants import HUB_ORIGIN
from machines.base.logic_machine import LogicMachine

class Hub(LogicMachine):
    def __init__(self, machine_data, rotation=0, origin=None):
        num_inputs = machine_data.size[0] * 2 + machine_data.size[1] * 2
        super().__init__(machine_data, num_inputs=num_inputs, rotation=rotation, origin=origin)
        self.storage: dict[TheoremKey, int] = {}

    def _to_key(self, item: Item | TheoremKey) -> TheoremKey:
        return item.key if isinstance(item, Item) else item

    def add(self, item: Item | TheoremKey, amount=1):
        key = self._to_key(item)
        self.storage[key] = self.storage.get(key, 0) + amount

    def remove(self, item: Item | TheoremKey, amount=1):
        key = self._to_key(item)
        if key in self.storage:
            self.storage[key] -= amount
            if self.storage[key] <= 0:
                del self.storage[key]


    def count(self, item: Item | TheoremKey) -> int:
        key = self._to_key(item)
        return self.storage.get(key, 0)
    

    def init_ports(self):
        """
        We just place ports along the border.
        This is simpler than dynamically changing the ports depending on the neighboring belts.
        """
        self.origin = HUB_ORIGIN
        origin_x, origin_y = self.origin
        size_x, size_y = self.size
        
        # corners
        self.add_port(Port(0, 0, Direction.WEST, "input"))
        self.add_port(Port(0, 0, Direction.WEST, "output"))
        self.add_port(Port(0, 0, Direction.NORTH, "input"))
        self.add_port(Port(0, 0, Direction.NORTH, "output"))

        self.add_port(Port(size_x-1, 0, Direction.EAST, "input"))
        self.add_port(Port(size_x-1, 0, Direction.EAST, "output"))
        self.add_port(Port(size_x-1, 0, Direction.NORTH, "input"))
        self.add_port(Port(size_x-1, 0, Direction.NORTH, "output"))

        self.add_port(Port(0, size_y-1, Direction.WEST, "input"))
        self.add_port(Port(0, size_y-1, Direction.WEST, "output"))
        self.add_port(Port(0, size_y-1, Direction.SOUTH, "input"))
        self.add_port(Port(0, size_y-1, Direction.SOUTH, "output"))
        
        self.add_port(Port(size_x-1, size_y-1, Direction.EAST, "input"))
        self.add_port(Port(size_x-1, size_y-1, Direction.EAST, "output"))
        self.add_port(Port(size_x-1, size_y-1, Direction.SOUTH, "input"))
        self.add_port(Port(size_x-1, size_y-1, Direction.SOUTH, "output"))

        # left line
        x = 0
        for y in range(1, size_y - 1):
            self.add_port(Port(x, y, Direction.WEST, "input"))
            self.add_port(Port(x, y, Direction.WEST, "output"))

        # right line
        x = size_x - 1
        for y in range(1, size_y - 1):
            self.add_port(Port(x, y, Direction.EAST, "input"))
            self.add_port(Port(x, y, Direction.EAST, "output"))

        # top line
        y = 0
        for x in range(1, size_x - 1):
            self.add_port(Port(x, y, Direction.NORTH, "input"))
            self.add_port(Port(x, y, Direction.NORTH, "output"))

        # bottom line
        y = size_y - 1
        for x in range(1, size_x - 1):
            self.add_port(Port(x, y, Direction.SOUTH, "input"))
            self.add_port(Port(x, y, Direction.SOUTH, "output"))


    def update(self, dt):
        super().update(dt)

    # IReceiver implementation
    def receive_item_at_port(self, item, port):
        self.add(item)
        # we need to store the input_offsets and input items for the slide-in-animation
        idx = self.input_ports.index(port)
        self.input_offsets[idx] = 0
        self.input_items[idx] = item
        return True

    # IProvider implementation
    def provide_item_from_port(self, port):
        pass

    def handle_backpressure(self, item, port):
        pass

    # custom output-function for the hub
    def provide_item_using_filter(self, port, filter: TheoremKey | None):
        if len(self.storage) == 0:
            return None

        if filter is None:
            return None
            # theorem_key, amount = self.storage.popitem()
            # if amount > 1:
            #     self.storage[theorem_key] = amount - 1
            #
            # item = Item(theorem_key.formula, is_theorem=theorem_key.is_theorem, assumptions=theorem_key.assumptions)
            # return item

        amount = self.storage.get(filter)
        if amount and amount >= 1:
            if amount == 1:
                self.storage.pop(filter)
            else:
                self.storage[filter] = amount - 1

            item = Item(filter.formula, is_theorem=filter.is_theorem, assumptions=filter.assumptions)
            return item
        return None

            

    # save and load logic
    def _add_custom_data(self, data):
        data["storage"] = [
            {"key": key.to_data(), "amount": amount} for key, amount in self.storage.items()
        ]


    def _load_custom_data(self, data):
        self.storage = {
            TheoremKey.from_data(entry["key"]): entry["amount"]
            for entry in data.get("storage", [])
        }

