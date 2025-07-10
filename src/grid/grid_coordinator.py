from grid.grid_manager import GridManager
from grid.update_system import UpdateSystem
from grid.grid_renderer import GridRenderer
from grid.item_transfer_system import ItemTransferSystem
from grid.connection_system import ConnectionSystem

class GridCoordinator:
    """Main coordinator for the grid system"""
    
    def __init__(self):
        self.grid_manager = GridManager()
        self.connection_system = ConnectionSystem(self.grid_manager)
        self.grid_manager.connection_system = self.connection_system
        self.item_transfer_system = ItemTransferSystem(self.grid_manager)
        self.update_system = UpdateSystem(self.grid_manager, self.item_transfer_system)
        self.renderer = GridRenderer(self.grid_manager)
    
    # Delegate common operations to grid_manager
    def add_block(self, grid_x: int, grid_y: int, block):
        self.grid_manager.add_block(grid_x, grid_y, block)
    
    def remove_block(self, grid_x: int, grid_y: int):
        return self.grid_manager.remove_block(grid_x, grid_y)
    
    def get_block(self, grid_x: int, grid_y: int):
        return self.grid_manager.get_block(grid_x, grid_y)
    
    def is_empty(self, grid_x: int, grid_y: int, size=(1, 1)):
        return self.grid_manager.is_empty(grid_x, grid_y, size)
    
    def update(self, dt: float):
        self.update_system.update(dt)
    
    def draw_grid_lines(self, screen, camera):
        self.renderer.draw_grid_lines(screen, camera)
    
    def draw_blocks(self, screen, camera):
        self.renderer.draw_blocks(screen, camera)
    
    def draw_items(self, screen, camera):
        self.renderer.draw_items(screen, camera)