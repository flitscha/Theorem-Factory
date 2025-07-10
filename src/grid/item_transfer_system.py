from entities.item import Item
from entities.port import Port

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