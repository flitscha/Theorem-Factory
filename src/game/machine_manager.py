from config.constants import *
from core.utils import get_grid_coordinates_when_placing_machine, get_mouse_grid_pos, can_overwrite_belt
from machines.types.generator import Generator
from machines.menu.generator_menu import GeneratorMenu
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from core.utils import get_mouse_grid_pos
from machines.types.binary_connective import BinaryConnective
from machines.menu.binary_connective_menu import BinaryConnectiveMenu

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

        # Check if there is already a block
        existing_blocks = self.grid.get_blocks_at_area(grid_x, grid_y, (rotated_size))

        if existing_blocks:
            # check if we can overwrite the existing block
            if machine_id == 'conveyor' and can_overwrite_belt(existing_blocks.get((grid_x, grid_y)), rotation):
                # Remove the existing block
                self.grid.remove_block(grid_x, grid_y)
            else:
                # if we cannot overwrite, do nothing
                return False

        # Place new machine
        machine = data.cls(data, rotation=rotation)
        self.grid.add_block(grid_x, grid_y, machine)
        return True
    
        
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
            if isinstance(block, Generator):
                return GeneratorMenu(screen, (500, 300), block)
            elif isinstance(block, BinaryConnective):
                return BinaryConnectiveMenu(screen, (500, 300), block)
                
        return None
    
    
    def get_machine_at_mouse(self):
        grid_x, grid_y = get_mouse_grid_pos(self.camera)
        machine = self.grid.get_block(grid_x, grid_y)
        return machine
    

    def rotate_machine_at_mouse(self):
        """Rotate the machine under the mouse cursor if any exists"""

        # get the grid-coordinates under the mouse
        grid_x, grid_y = get_mouse_grid_pos(self.camera)

        machine = self.grid.get_block(grid_x, grid_y)
        if not machine:
            return False

        # update the neighboring belts, BEFORE rotating
        self.grid.connection_system.update_neighboring_belts_when_removing(machine)

        # rotate the machine
        machine.rotate(1)
        machine.clear_ports()
        machine.init_ports()
        machine.rotate_ports()

        # if the machine is a conveyor belt, we have to do more. We have to reset the ports, inputs and outputs
        if isinstance(machine, ConveyorBelt):
            machine.inputs = []
            machine.outputs = []
            self.grid.connection_system.handle_placing_conveyor_belt(machine)

        # update the connections
        self.grid.connection_system.update_neighboring_belts_when_placing(machine)
        self.grid.connection_system.update_connections_at(grid_x, grid_y)
        return True