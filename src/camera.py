import pygame

from settings import *


class Camera():
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
    
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
    
    def update(self, keys):
        move_x = 0
        move_y = 0

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

        self.move(move_x, move_y)