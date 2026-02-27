import pygame

from config.constants import TILE_SIZE, CAMERA_ZOOM_FACTOR, CAMERA_MIN_ZOOM, CAMERA_MAX_ZOOM, CAMERA_SPEED
from core.utils import get_mouse_world_pos
from typing import Tuple

class Camera():
    def __init__(self):
        # the camera offset is the world coordinates of the top-left corner of the screen
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0

        self.mouse_pos = pygame.mouse.get_pos()
        self.last_mouse_pos = (0, 0) # mouse-position, one frame before. (needed for drag-and-drop-feature)
    
    def get_visible_tile_bounds(self) -> Tuple[int, int, int, int]:
        """Get the bounds of the visible area in tile coordinates"""
        w, h = pygame.display.get_surface().get_size()
        left = int(self.offset_x // TILE_SIZE)
        top = int(self.offset_y // TILE_SIZE)
        right = int((self.offset_x + w / self.zoom) // TILE_SIZE) + 1
        bottom = int((self.offset_y + h / self.zoom) // TILE_SIZE) + 1
        return left, right, top, bottom

    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
    

    def change_zoom(self, zoom_dir):
        mouse_world_x, mouse_world_y = get_mouse_world_pos(self)

        if zoom_dir > 0:  # Zoom in
            self.zoom *= (1 + CAMERA_ZOOM_FACTOR)
        elif zoom_dir < 0:  # Zoom out
            self.zoom *= (1 - CAMERA_ZOOM_FACTOR)
        
        # Clamp zoom level
        self.zoom = max(CAMERA_MIN_ZOOM, min(self.zoom, CAMERA_MAX_ZOOM))

        # calculate new offset, such that the mouse position remains the same in world coordinates
        self.offset_x = mouse_world_x - (self.mouse_pos[0] / self.zoom)
        self.offset_y = mouse_world_y - (self.mouse_pos[1] / self.zoom)


    def handle_mouse_wheel(self, zoom_dir):
        if zoom_dir != 0 and self.mouse_pos is not None:
            self.change_zoom(zoom_dir)


    def handle_dragging(self, is_dragging):
        if is_dragging:
            dx = self.mouse_pos[0] - self.last_mouse_pos[0]
            dy = self.mouse_pos[1] - self.last_mouse_pos[1]

            self.offset_x -= dx / self.zoom
            self.offset_y -= dy / self.zoom

        
    def handle_wasd(self, keys):
        move_x = 0
        move_y = 0
        if pygame.K_LEFT in keys or pygame.K_a in keys:
            move_x += -CAMERA_SPEED
        if pygame.K_RIGHT in keys or pygame.K_d in keys:
            move_x += CAMERA_SPEED
        if pygame.K_UP in keys or pygame.K_w in keys:
            move_y += -CAMERA_SPEED
        if pygame.K_DOWN in keys or pygame.K_s in keys:
            move_y += CAMERA_SPEED
        
        # normalize movement to ensure consistent speed (when moving diagonally)
        if move_x != 0 and move_y != 0:
            move_x /= 2**0.5
            move_y /= 2**0.5

        self.move(move_x, move_y)


    def update(self):
        self.last_mouse_pos = self.mouse_pos
        self.mouse_pos = pygame.mouse.get_pos()
        
        


