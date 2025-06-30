import pygame

from config.settings import *
from core.utils import get_mouse_world_pos

class Camera():
    def __init__(self):
        # the camera offset is the world coordinates of the top-left corner of the screen
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0

        self.mouse_pos = pygame.mouse.get_pos()
        self.last_mouse_pos = (0, 0) # mouse-position, one frame before. (needed for drag-and-drop-feature)
    
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


    def update(self, keys, zoom_dir, is_dragging):
        self.last_mouse_pos = self.mouse_pos
        self.mouse_pos = pygame.mouse.get_pos()
        move_x = 0
        move_y = 0

        # movement with arrow keys or WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x += -CAMERA_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += CAMERA_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y += -CAMERA_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += CAMERA_SPEED
        
        # normalize movement to ensure consistent speed (when moving diagonally)
        if move_x != 0 and move_y != 0:
            move_x /= 2**0.5
            move_y /= 2**0.5
        
        # Maus-Drag movement
        if is_dragging:
            dx = self.mouse_pos[0] - self.last_mouse_pos[0]
            dy = self.mouse_pos[1] - self.last_mouse_pos[1]

            self.offset_x -= dx / self.zoom
            self.offset_y -= dy / self.zoom

        # zoom with mouse wheel
        if zoom_dir != 0 and self.mouse_pos is not None:
            self.change_zoom(zoom_dir)

        self.move(move_x, move_y)