import pygame

from settings import *
from utils import screen_to_world, world_to_screen

class Camera():
    def __init__(self):
        # the camera offset is the world coordinates of the top-left corner of the screen
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
    
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
    

    def change_zoom(self, zoom_dir, mouse_pos):
        mouse_world_x, mouse_world_y = screen_to_world(*mouse_pos, self.offset_x, self.offset_y, self.zoom)

        if zoom_dir > 0:  # Zoom in
            self.zoom *= (1 + CAMERA_ZOOM_FACTOR)
        elif zoom_dir < 0:  # Zoom out
            self.zoom *= (1 - CAMERA_ZOOM_FACTOR)
        
        # Clamp zoom level
        self.zoom = max(CAMERA_MIN_ZOOM, min(self.zoom, CAMERA_MAX_ZOOM))

        # calculate new offset, such that the mouse position remains the same in world coordinates
        self.offset_x = mouse_world_x - (mouse_pos[0] / self.zoom)
        self.offset_y = mouse_world_y - (mouse_pos[1] / self.zoom)


    def update(self, keys, zoom_dir, mouse_pos, last_mouse_pos, is_dragging):
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
            dx = mouse_pos[0] - last_mouse_pos[0]
            dy = mouse_pos[1] - last_mouse_pos[1]

            self.offset_x -= dx / self.zoom
            self.offset_y -= dy / self.zoom

        # zoom with mouse wheel
        if zoom_dir != 0 and mouse_pos is not None:
            self.change_zoom(zoom_dir, mouse_pos)

        self.move(move_x, move_y)