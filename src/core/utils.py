import pygame

from config.settings import TILE_SIZE


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



def get_grid_coordinates_when_placing_machine(camera, machine_size, mouse_pos=None):
    """Get the grid coordinates where a machine would be placed based on the mouse position."""

    world_x, world_y = get_mouse_world_pos(camera, mouse_pos)
    
    # Calculate the grid position based on world coordinates
    world_x -= (machine_size[0] * TILE_SIZE) / 2
    world_y -= (machine_size[1] * TILE_SIZE) / 2
    grid_x = round(world_x / TILE_SIZE)
    grid_y = round(world_y / TILE_SIZE)

    return grid_x, grid_y



def grid_to_screen_coordinates(grid_x, grid_y, camera):
    """Convert grid coordinates to screen coordinates based on camera offset."""
    
    world_x = grid_x * TILE_SIZE
    world_y = grid_y * TILE_SIZE

    screen_x, screen_y = world_to_screen(world_x, world_y, camera)
    
    return screen_x, screen_y