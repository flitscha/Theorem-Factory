from typing import Dict, Tuple
from grid.grid_manager import GridManager
from grid.update_system import UpdateSystem
from grid.grid_renderer import GridRenderer
from grid.item_transfer_system import ItemTransferSystem
from grid.connection_system import ConnectionSystem
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine
from machines.types.conveyor_belt.belt_autoconnect import ConveyorBeltAutoConnector

class GridCoordinator:
    """Main coordinator for the grid system"""
    
    def __init__(self):
        self.grid_manager = GridManager()
        self.connection_system = ConnectionSystem(self.grid_manager)
        self.item_transfer_system = ItemTransferSystem(self.grid_manager)
        self.update_system = UpdateSystem(self.grid_manager, self.item_transfer_system)
        self.renderer = GridRenderer(self.grid_manager)
    
    # Delegate common operations to grid_manager
    def add_block(self, grid_x: int, grid_y: int, block):
        self.grid_manager.add_block(grid_x, grid_y, block)

        # update connections for the newly placed block
        self.connection_system.update_connections_at(grid_x, grid_y)

        # if the block is a conveyor belt, update its inputs and outputs
        if isinstance(block, ConveyorBelt):
            self.connection_system.handle_placing_conveyor_belt(block)
            # the neighboring belts are getting updated inside handle_placing_conveyor_belt()
        else:
            # update neighboring belts
            self.connection_system.update_neighboring_belts_when_placing(block)
        
    
    def remove_block(self, grid_x: int, grid_y: int):
        # Update connections before removing the block
        block = self.grid_manager.get_block(grid_x, grid_y)
        if block:
            self.connection_system.update_neighboring_belts_when_removing(block)
        return self.grid_manager.remove_block(grid_x, grid_y)
    
    def get_block(self, grid_x: int, grid_y: int):
        return self.grid_manager.get_block(grid_x, grid_y)
    
    def get_blocks_at_area(self, grid_x: int, grid_y: int, size: tuple[int, int]) -> Dict[Tuple[int, int], Machine]:
        return self.grid_manager.get_blocks_at_area(grid_x, grid_y, size)
    
    def get_neighboring_machines(self, grid_x: int, grid_y: int):
        return self.grid_manager.get_neighboring_machines(grid_x, grid_y)
    
    def get_neighboring_machines_of(self, machine: Machine):
        return self.grid_manager.get_neighboring_machines_of(machine)
    
    def is_empty(self, grid_x: int, grid_y: int, size=(1, 1)):
        return self.grid_manager.is_empty(grid_x, grid_y, size)
    
    def update(self, dt: float):
        self.update_system.update(dt)
    
    def draw_grid_lines(self, screen, camera):
        self.renderer.draw_grid_lines(screen, camera)
    
    def draw_machines(self, screen, camera):
        self.renderer.draw_machines(screen, camera)
    
    def draw_highlight(self, screen, camera, active_tool):
        self.renderer.draw_highlight(screen, camera, active_tool, self.grid_manager)
    
    def draw_items(self, screen, camera):
        self.renderer.draw_items(screen, camera)
    
    def draw_conveyor_belts(self, screen, camera):
        self.renderer.draw_conveyor_belts(screen, camera)