from typing import List, Optional
from entities.item import Item
from grid.interfaces import IConveyorNode, IItemAcceptor

class ConveyorSystem:
    """Handles item movement between conveyor belts"""
    
    def __init__(self, grid_manager):
        self.grid_manager = grid_manager
        self.loose_items: List[Item] = []  # Items that couldn't be placed
    
    def update(self, dt: float):
        """Update the conveyor system"""
        # Process all conveyor nodes that are ready to output
        for conveyor in list(self.grid_manager.conveyor_nodes):
            if conveyor.is_ready_to_output():
                self._try_move_item(conveyor)
    
    def _try_move_item(self, conveyor: IConveyorNode):
        """Try to move an item from one conveyor to the next"""
        item = conveyor.try_output_item()
        if not item:
            return
        
        # Get target position
        target_pos = conveyor.get_output_position()
        target_block = self.grid_manager.get_block(target_pos[0], target_pos[1])
        
        # Try to place item
        if target_block and isinstance(target_block, (IConveyorNode, IItemAcceptor)):
            if target_block.try_accept_item(item):
                return  # Successfully moved
        
        # Couldn't place item - handle backpressure
        self._handle_backpressure(conveyor, item)
    
    def _handle_backpressure(self, conveyor: IConveyorNode, item: Item):
        """Handle when an item can't be moved forward"""
        # Try to put item back on the conveyor
        if not conveyor.try_accept_item(item):
            # If that fails, add to loose items (shouldn't happen normally)
            self.loose_items.append(item)
    
    def add_loose_item(self, item: Item):
        """Add an item that couldn't be placed anywhere"""
        print(f"Adding loose item: {item.formula} at {item.position}")
        self.loose_items.append(item)
    
    def get_loose_items(self) -> List[Item]:
        """Get all loose items for rendering"""
        return self.loose_items.copy()