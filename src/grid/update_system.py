from grid.interfaces import IUpdatable

class UpdateSystem:
    """Coordinates updates for all grid objects"""
    
    def __init__(self, grid_manager, item_transfer_system):
        self.grid_manager = grid_manager
        self.item_transfer_system = item_transfer_system
    
    def update(self, dt: float):
        """Update all systems"""
        # Update all updatable blocks
        for block in self.grid_manager.blocks.values():
            if isinstance(block, IUpdatable):
                # Call update method if block implements IUpdatable
                block.update(dt)
        
        # Update item transfer system
        self.item_transfer_system.update(dt)
