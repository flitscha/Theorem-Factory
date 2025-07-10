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