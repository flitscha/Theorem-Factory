import pygame

from config.settings import TILE_SIZE
from core.utils import get_grid_coordinates_when_placing_machine, grid_to_screen_coordinates, can_overwrite_belt
from config.settings import SCREEN_HEIGHT, MACHINE_SELECTION_GUI_HEIGHT
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.types.conveyor_belt.belt_autoconnect import ConveyorBeltAutoConnector

class PlacementPreview():
    def __init__(self, screen, grid, camera, machine_database):
        self.grid = grid
        self.screen = screen
        self.camera = camera
        self.machine_database = machine_database

        # if you are in build-mode, you can see a preview of the machine you are about to place
        self.active_preview = None # the ID of the machine to preview, or None if no preview is active 
        self.rotation = 0  # rotation state: 0,1,2,3 (each *90 degrees)

    def start_preview(self, machine_id):
        self.active_preview = machine_id
        self.rotation = 0

    def stop_preview(self):
        self.active_preview = None
        self.rotation = 0  # reset rotation on new preview
    
    def rotate_preview(self):
        if self.active_preview is not None:
            self.rotation = (self.rotation + 1) % 4  # cycle 0->1->2->3->0
    
    # --------- Helper functions for drawing -----------
    def _get_rotated_size(self, size):
        """Get the size of the machine after rotation"""
        return (size[1], size[0]) if self.rotation % 2 == 1 else size

    def _create_dummy_machine(self, data, grid_x, grid_y):
        """Create a dummy machine for preview purposes"""
        dummy = data.cls(data)
        dummy.rotation = self.rotation
        dummy.origin = (grid_x, grid_y)

        # configure the dummy machine, if it is a conveyor belt
        if isinstance(dummy, ConveyorBelt):
            neighbors = self.grid.get_neighboring_machines(grid_x, grid_y)
            ConveyorBeltAutoConnector.configure(dummy, neighbors, self.grid.connection_system)
            ConveyorBeltAutoConnector.update_sprite(dummy)
            # right now, we don't update the sprites of the neighbors. But this would also be an option.

        #dummy.rotate_image()
        return dummy

    def _draw_overlay(self, surface, grid_x, grid_y):
        """Draw an overlay on the surface (red or yellow) to indicate placement validity"""
        existing_block = self.grid.get_block(grid_x, grid_y)

        if existing_block is None:
            return  # no overlay if space is free
        elif can_overwrite_belt(existing_block, self.rotation):
            # Yellow overlay for overwriting
            yellow_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            yellow_overlay.fill((255, 255, 0, 120))
            surface.blit(yellow_overlay, (0, 0))
        else:
            # Red overlay for invalid placement
            red_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 120))
            surface.blit(red_overlay, (0, 0))

    # --------- Main draw function -----------
    def draw(self):
        if pygame.mouse.get_pos()[1] > SCREEN_HEIGHT - MACHINE_SELECTION_GUI_HEIGHT:
            return
        
        if not self.active_preview:
            return
        
        # Get the machine data
        data = self.machine_database.get(self.active_preview)
        rotated_size = self._get_rotated_size(data.size)
        grid_x, grid_y = get_grid_coordinates_when_placing_machine(self.camera, rotated_size)
        screen_x, screen_y = grid_to_screen_coordinates(grid_x, grid_y, self.camera)

        # Create a dummy machine for preview
        dummy_machine = self._create_dummy_machine(data, grid_x, grid_y)

        # draw the sprite of the dummy machine
        scaled_image = pygame.transform.scale(
            dummy_machine.image,
            (int(rotated_size[0] * TILE_SIZE * self.camera.zoom),
             int(rotated_size[1] * TILE_SIZE * self.camera.zoom))
        )
        overlay_surface = scaled_image.copy()
        overlay_surface.set_alpha(90)

        # add the overlay (yellow/red)
        self._draw_overlay(overlay_surface, grid_x, grid_y)

        # Draw it on the screen
        self.screen.blit(overlay_surface, (screen_x, screen_y))

        """
        data = self.machine_database.get(self.active_preview)
        image = data.image
        size = data.size

        # Calculate rotated size. (swap the x-size and y-size)
        if self.rotation % 2 == 1:  # 90 or 270 degrees
            rotated_size = (size[1], size[0])
        else:
            rotated_size = size

        # calculate the grid position
        grid_x, grid_y = get_grid_coordinates_when_placing_machine(self.camera, rotated_size)
        screen_x, screen_y = grid_to_screen_coordinates(grid_x, grid_y, self.camera)

        # Rotate the image
        angle = self.rotation * 90
        rotated_image = pygame.transform.rotate(image, -angle)  # negative to rotate clockwise

        # Scale the rotated image
        scaled_image = pygame.transform.scale(
            rotated_image, 
            (int(rotated_size[0] * TILE_SIZE * self.camera.zoom), 
                int(rotated_size[1] * TILE_SIZE * self.camera.zoom))
        )

        # Semi-transparent machen (alpha)
        overlay_surface = scaled_image.copy()

        overlay_surface.set_alpha(90)  # normal preview alpha

        # Determine color: no color / yellow / red
        existing_block = self.grid.get_block(grid_x, grid_y)

        if existing_block is None:
            # space is free -> no overlay
            pass
        elif can_overwrite_belt(existing_block, self.rotation):
            # yellow overlay for overwriting
            yellow_overlay = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
            yellow_overlay.fill((255, 255, 0, 120))
            overlay_surface.blit(yellow_overlay, (0, 0))
        else:
            # red overlay for invalid placement
            red_overlay = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 120))
            overlay_surface.blit(red_overlay, (0, 0))

        self.screen.blit(overlay_surface, (screen_x, screen_y))"""