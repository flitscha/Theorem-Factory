from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.types.conveyor_belt.belt_autoconnect import ConveyorBeltAutoConnector
from machines.base.machine import Machine


class ConnectionSystem:
    """Handles connections between blocks in the grid"""
    def __init__(self, grid_manager):
        self.grid_manager = grid_manager

    def update_connections_at(self, grid_x: int, grid_y: int):
        """Re-evaluate connections for the block at (x, y) and its neighbors"""
        block = self.grid_manager.get_block(grid_x, grid_y)
        if not block:
            return

        # Check for output ports -> scan neighbor tiles for valid inputs
        if hasattr(block, "output_ports"):
            for port in block.output_ports:
                target_pos = port.get_connection_position()
                target = self.grid_manager.get_block(*target_pos)
                if target and hasattr(target, "input_ports"):
                    port.connect_if_possible(target)

        # Do the same for input_ports
        if hasattr(block, "input_ports"):
            for port in block.input_ports:
                source_pos = port.get_connection_position()
                source = self.grid_manager.get_block(*source_pos)
                if source and hasattr(source, "output_ports"):
                    port.connect_if_possible(source)



    def handle_placing_conveyor_belt(self, conveyor: ConveyorBelt):
        # 1) determine inputs and outputs based on neighboring belts (and machines)
        # we can use the simple neighbor-function here, because a conveyor belt is only 1x1 tile
        neighboring_machines = self.grid_manager.get_neighboring_machines(conveyor.origin[0], conveyor.origin[1])

        # 2) configure the conveyor belt based on its neighbors
        ConveyorBeltAutoConnector.configure(conveyor, neighboring_machines, self)

        # 3) update the neighboring belts
        for direction, neighbor in neighboring_machines.items():
            if neighbor and isinstance(neighbor, ConveyorBelt):
                ConveyorBeltAutoConnector.configure_neighbor_when_placing(neighbor, direction, conveyor, self)
                self.update_connections_at(neighbor.origin[0], neighbor.origin[1])
        
        # 4) update the sprite of the conveyor belt
        ConveyorBeltAutoConnector.update_sprite(conveyor)


    def update_neighboring_belts_when_placing(self, machine: Machine):
        neighboring_machines = self.grid_manager.get_neighboring_machines_of(machine)
        for direction, neighbors in neighboring_machines.items():
            for neighbor in neighbors:
                if isinstance(neighbor, ConveyorBelt):
                    ConveyorBeltAutoConnector.configure_neighbor_when_placing(neighbor, direction, machine, self)
                    self.update_connections_at(neighbor.origin[0], neighbor.origin[1])


    def update_neighboring_belts_when_removing(self, machine: Machine):
        """Update neighboring belts, when a block is removed"""
        # Get neighboring conveyors
        neighboring_machines = self.grid_manager.get_neighboring_machines_of(machine)
        for direction, neighbors in neighboring_machines.items():
            for neighbor in neighbors:
                if isinstance(neighbor, ConveyorBelt):
                    ConveyorBeltAutoConnector.configure_neighbor_when_removing(neighbor, direction, machine, self)
                    self.update_connections_at(neighbor.origin[0], neighbor.origin[1])
    