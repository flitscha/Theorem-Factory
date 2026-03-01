from entities.item import Item
from entities.port import Port
from machines.types.conveyor_belt.output_belt import OutputBelt
from machines.types.hub import Hub

class ItemTransferSystem:
    """Handles item transfers between connected ports."""

    def __init__(self, grid_manager):
        self.grid_manager = grid_manager

    def update(self, dt: float):
        """Main update loop – processes all transfers"""
        self._process_all_ports()
        # pending system?

    def _process_all_ports(self):
        """Scan grid and handle transfers from all output ports"""
        for block in self.grid_manager.blocks.values():
            if not hasattr(block, "output_ports"):
                continue
            
            # handle the connections from the hub to an OutputBelt
            if isinstance(block, OutputBelt) and block.is_active and not block.item:
                filter = block.output_filter
                for input_port in block.input_ports:
                    connected_port = input_port.connected_port
                    if connected_port and isinstance(connected_port.machine, Hub):
                        item = connected_port.machine.provide_item_using_filter(connected_port, filter)

                        if not item:
                            continue

                        if not input_port.receive_item(item):
                            self._handle_backpressure(connected_port, item)

            
            # every other connection
            for output_port in block.output_ports:
                # Try to get an item from this output port
                item = output_port.provide_item()
                if item is None:
                    continue

                target_port = output_port.connected_port
                if target_port is None:
                    # No connection, drop the item
                    self._handle_backpressure(output_port, item)
                    continue

                # Try to send the item to the connected input port
                if not target_port.receive_item(item):
                    # Target not ready – reinsert or queue
                    self._handle_backpressure(output_port, item)

    
    def _handle_backpressure(self, output_port: Port, item: Item):
        """Let the source machine handle it – or queue it for retry"""
        machine = output_port.machine
        if hasattr(machine, "handle_backpressure"):
            machine.handle_backpressure(item, output_port)
        else:
            # Fallback: queue for retry if no logic defined?
            if output_port.connected_port:
                print("Warning: Output port has no backpressure logic defined.")
