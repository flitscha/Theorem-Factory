import pygame

from config.constants import TILE_SIZE


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


def get_mouse_grid_pos(camera, mouse_pos=None):
    mouse_world_x, mouse_world_y = get_mouse_world_pos(camera, mouse_pos)
    grid_x = int(mouse_world_x // TILE_SIZE)
    grid_y = int(mouse_world_y // TILE_SIZE)
    return grid_x, grid_y


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


def can_overwrite_belt(existing_block, new_rotation):
    from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt

    if not existing_block:
        return False
    
    # Only belts
    if not isinstance(existing_block, ConveyorBelt):
        return False
     
    # if the direction is the same, do nothing
    if existing_block.rotation == new_rotation:
        return False
    
    # if the direction is opposite AND the existing belt is straight, do nothing
    if (existing_block.rotation + 2) % 4 == new_rotation and \
            existing_block.input_ports[0].direction == existing_block.output_ports[0].direction.opposite():
        return False

    # all other cases: the existing belt can be overwritten
    return True



def simplify_formula(formula: str) -> str:
    """
    remove unnecessary brackets.
    Example: "((A + B))"        ->      "A + B"
    Example: "(A + (B * (-C)))" ->      "A + B * -C"
    Example: "(A * ((-B) + C)"  ->      "A * (-B + C)"    
    """
    formula = formula.strip()

    # remove outer brackets
    while formula.startswith("(") and formula.endswith(")"):
        inner = formula[1:-1].strip()
        depth = 0
        valid = True

        for i, c in enumerate(inner):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1

            if depth < 0 or (depth == 0 and i != len(inner) - 1):
                valid = False
                break

        if valid:
            formula = inner
        else:
            break

    return formula
