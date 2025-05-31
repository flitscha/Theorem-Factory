import pygame

def screen_to_world(screen_x, screen_y, camera):
    """Convert screen coordinates to world coordinates based on camera offset."""
    
    world_x = camera.offset_x + screen_x / camera.zoom
    world_y = camera.offset_y + screen_y / camera.zoom

    return world_x, world_y


def get_mouse_world_pos(camera, mouse_pos=None):
    if mouse_pos is None:
        mouse_pos = pygame.mouse.get_pos()

    mouse_world_x, mouse_world_y = screen_to_world(*mouse_pos, camera)
    return mouse_world_x, mouse_world_y


def world_to_screen(world_x, world_y, camera):
    """Convert world coordinates to screen coordinates based on camera offset."""
    
    screen_x = (world_x - camera.offset_x) * camera.zoom
    screen_y = (world_y - camera.offset_y) * camera.zoom

    return screen_x, screen_y
