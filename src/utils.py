import pygame

def screen_to_world(screen_x, screen_y, camera_offset_x, camera_offset_y, camera_zoom):
    """Convert screen coordinates to world coordinates based on camera offset."""
    
    world_x = camera_offset_x + screen_x / camera_zoom
    world_y = camera_offset_y + screen_y / camera_zoom

    return world_x, world_y


def get_mouse_world_pos(camera, mouse_pos=None):
    if mouse_pos is None:
        mouse_pos = pygame.mouse.get_pos()

    mouse_world_x, mouse_world_y = screen_to_world(
        *mouse_pos, camera.offset_x, camera.offset_y, camera.zoom
    )
    return mouse_world_x, mouse_world_y


def world_to_screen(world_x, world_y, camera_offset_x, camera_offset_y, camera_zoom):
    """Convert world coordinates to screen coordinates based on camera offset."""
    
    screen_x = (world_x - camera_offset_x) * camera_zoom
    screen_y = (world_y - camera_offset_y) * camera_zoom

    return screen_x, screen_y
