import pygame

from settings import TILE_SIZE
from utils import get_grid_coordinates_when_placing_machine, grid_to_screen_coordinates
from settings import SCREEN_HEIGHT, MACHINE_SELECTION_GUI_HEIGHT

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

    def draw(self):
        if pygame.mouse.get_pos()[1] > SCREEN_HEIGHT - MACHINE_SELECTION_GUI_HEIGHT:
            return
        
        if self.active_preview:
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
            overlay_surface.set_alpha(90)

            self.screen.blit(overlay_surface, (screen_x, screen_y))