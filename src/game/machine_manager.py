from config.settings import *
from core.utils import get_grid_coordinates_when_placing_machine, get_mouse_grid_pos
from machines.types.generator import Generator
from machines.menu.generator_menu import GeneratorMenu

class MachineManager:
    """Handles all machine-related operations. 
    Currently supports placing and removing machines, and opening machine menus."""
    
    def __init__(self, grid, camera, placement_preview, machine_database):
        self.grid = grid
        self.camera = camera
        self.placement_preview = placement_preview
        self.machine_database = machine_database
        
    def try_place_machine(self, mouse_pos):
        """Attempt to place a machine at the given position"""
        # Don't place if clicking on GUI area
        if mouse_pos[1] > SCREEN_HEIGHT - MACHINE_SELECTION_GUI_HEIGHT:
            return False
            
        machine_id = self.placement_preview.active_preview
        rotation = self.placement_preview.rotation
        
        if not machine_id:
            return False
            
        # Get machine data and calculate rotated size
        data = self.machine_database.get(machine_id)
        size = data.size
        
        rotated_size = (size[1], size[0]) if rotation % 2 == 1 else size
        grid_x, grid_y = get_grid_coordinates_when_placing_machine(self.camera, rotated_size)
        
        # Check if position is empty and place machine
        if self.grid.is_empty(grid_x, grid_y, rotated_size):
            machine = data.cls(data, rotation=rotation)
            self.grid.add_block(grid_x, grid_y, machine)
            return True
            
        return False
        
    def remove_machine_at_mouse(self):
        """Remove machine at current mouse position"""
        grid_x, grid_y = get_mouse_grid_pos(self.camera)
        self.grid.remove_block(grid_x, grid_y)
        
    def create_menu_for_machine_at_mouse(self, screen):
        """Create appropriate menu for machine at mouse position"""
        if self.placement_preview.active_preview:
            return None
            
        grid_x, grid_y = get_mouse_grid_pos(self.camera)
        block = self.grid.get_block(grid_x, grid_y)
        
        if block:
            # TODO: Make this more generic with a registry system
            if isinstance(block, Generator):
                return GeneratorMenu(screen, (500, 300), block)
                
        return None