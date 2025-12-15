from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine
from machines.base.logic_machine import LogicMachine
from entities.item import Item
from machines.base.machine_database import MachineDatabase


class MachineFactory:
    """Helper to create machines from saved data"""
    
    @staticmethod
    def from_data(data: dict, machine_database: MachineDatabase) -> Machine:
        machine_type = data["type"]
        origin = tuple(data.get("origin", (0, 0)))
        rotation = data.get("rotation", 0)

        machine_data = machine_database.get(machine_type)
        if not machine_data:
            raise ValueError(f"Unknown machine type: {machine_type}")

        cls = machine_data.cls
        machine = cls(machine_data, rotation=rotation)
        machine.origin = origin

        # restore items
        MachineFactory._load_items(machine, data)

        # restore machine-specific selections / state
        if hasattr(machine, "_load_custom_data"):
            machine._load_custom_data(data)

        return machine

    @staticmethod
    def _load_items(machine: Machine, data: dict):
        """Restore items for conveyors or logic machines"""
        # ConveyorBelt
        if hasattr(machine, "item"):
            item_data = data.get("item")
            if item_data:
                machine.item = Item.from_data(item_data["data"])
                machine.item_progress = item_data.get("progress", 0.0)
        # LogicMachine
        if hasattr(machine, "input_items") and hasattr(machine, "output_item"):
            items_data = data.get("items", {})
            inputs = items_data.get("inputs", [])
            machine.input_items = [Item.from_data(i) if i else None for i in inputs]
            output_data = items_data.get("output")
            machine.output_item = Item.from_data(output_data) if output_data else None
            machine.timer = items_data.get("progress", 0.0)
