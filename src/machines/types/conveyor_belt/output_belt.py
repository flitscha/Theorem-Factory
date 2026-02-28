from config.constants import HUB_ORIGIN, HUB_SIZE
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from core.theorem_key import TheoremKey
from entities.port import Port
from entities.item import Item

class OutputBelt(ConveyorBelt):
    """
    This is used to export items from the hub.
    It acts like an conveyor belt, but the player can select which item gets exprted from the hub.
    """
    
    def __init__(self, machine_data, rotation=0, origin=None):
        super().__init__(machine_data, rotation=rotation, origin=origin)
        # We use this class like this: each belt next to the hub is made into an output_belt.
        # However only belts that are hub-outputs act like OutputBelt. Otherwise it is just like a normal ConveyorBelt.
        self.is_active = self._is_output_of_hub()
        self.output_filter: TheoremKey | None = None

    def set_filter(self, item: TheoremKey | None):
        self.output_filter = item


    # override the rotate-function
    def rotate(self, n=1):
        super().rotate(n=n)
        self.is_active = self._is_output_of_hub()

    def _is_output_of_hub(self) -> bool:
        hub_origin_x, hub_origin_y = HUB_ORIGIN
        hub_size_x, hub_size_y = HUB_SIZE

        hub_min_x = hub_origin_x
        hub_max_x = hub_origin_x + hub_size_x - 1
        hub_min_y = hub_origin_y
        hub_max_y = hub_origin_y + hub_size_y - 1

        x, y = self.origin

        if x == hub_min_x - 1 and hub_min_y <= y <= hub_max_y:
            return self.rotation != 0 # TODO: get rid of the horrible numbers

        if x == hub_max_x + 1 and hub_min_y <= y <= hub_max_y:
            return self.rotation != 2

        if y == hub_min_y - 1 and hub_min_x <= x <= hub_max_x:
            return self.rotation != 1

        if y == hub_max_y + 1 and hub_min_x <= x <= hub_max_x:
            return self.rotation != 3

        return False

    
    def receive_item_at_port(self, item: Item, port: Port) -> bool:
        if self.output_filter is not None and self.output_filter != item.key:
            return False
        return super().receive_item_at_port(item, port)
