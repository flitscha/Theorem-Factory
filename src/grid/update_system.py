from typing import List
from entities.item import Item
from grid.interfaces import IUpdatable, IItemProducer

class UpdateSystem:
    """Coordinates updates for all grid objects"""
    
    def __init__(self, grid_manager, conveyor_system):
        self.grid_manager = grid_manager
        self.conveyor_system = conveyor_system
    
    def update(self, dt: float):
        """Update all systems"""
        # Update all updatable blocks
        for block in list(self.grid_manager.updatable_blocks):
            result = block.update(dt)
            if result:  # Block produced an item that couldn't be placed
                pass
                #self.conveyor_system.add_loose_item(result)
        
        # Update conveyor system
        self.conveyor_system.update(dt)
        
        # Handle item producers
        self._update_producers()
    
    def _update_producers(self):
        """Update item producers"""
        for producer in list(self.grid_manager.item_producers):
            item = producer.try_produce_item()
            if item:
                # Try to place item on adjacent conveyor
                pass
