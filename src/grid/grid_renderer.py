import pygame
import math
import time
from config.constants import TILE_SIZE, GRID_LINE_COLOR
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from core.utils import get_mouse_grid_pos, grid_to_screen_coordinates

class GridRenderer:
    """Handles rendering of the grid and its contents"""
    
    def __init__(self, grid_manager):
        self.grid_manager = grid_manager
    
    def draw_grid_lines(self, screen, camera):
        """Draw the grid lines"""
        screen_width, screen_height = screen.get_size()
        start_x = int(-(camera.offset_x % TILE_SIZE) * camera.zoom)
        start_y = int(-(camera.offset_y % TILE_SIZE) * camera.zoom)
        
        # Vertical lines
        x = start_x
        while x < screen_width:
            pygame.draw.line(screen, GRID_LINE_COLOR, (int(x), 0), (int(x), screen_height))
            x += TILE_SIZE * camera.zoom
        
        # Horizontal lines
        y = start_y
        while y < screen_height:
            pygame.draw.line(screen, GRID_LINE_COLOR, (0, int(y)), (screen_width, int(y)))
            y += TILE_SIZE * camera.zoom
    
    def _block_is_visible(self, block, camera) -> bool:
        """Check if the block is within the visible bounds of the camera"""
        min_x, max_x, min_y, max_y = camera.get_visible_tile_bounds()
        tile_x, tile_y = block.origin
        w, h = block.size
        
        return not (tile_x + w < min_x or tile_x > max_x or tile_y + h < min_y or tile_y > max_y)


    def draw_machines(self, screen, camera):
        """Draw all blocks on the grid, that are not conveyor belts"""
        for (tile_x, tile_y), block in self.grid_manager.blocks.items():
            # Check if block is within visible bounds
            if not self._block_is_visible(block, camera):
                continue

            # Draw the block
            if not isinstance(block, ConveyorBelt):
                block.draw(screen, camera)
    

    def draw_highlight(self, screen, camera, active_tool, grid_manager):
        """Draw a highlight depending on the current tool (e.g., eraser, empty tool)"""
        grid_x, grid_y = get_mouse_grid_pos(camera)
        block = grid_manager.get_block(grid_x, grid_y)
        if not block:
            return

        screen_x, screen_y = grid_to_screen_coordinates(block.origin[0], block.origin[1], camera)
        block_width = block.size[0] * TILE_SIZE * camera.zoom
        block_height = block.size[1] * TILE_SIZE * camera.zoom

        # select alpha, and color, based on tool
        if active_tool == "eraser":
            alpha = 80 + int(20 * math.sin(time.time() * 5))
            base_color = (255, 50, 50)
        elif active_tool == "None":
            alpha = 90 + int(20 * math.sin(time.time() * 5))
            base_color = (200, 200, 200)
        else:
            return

        sprite = block.image
        if sprite is None:
            return
        sprite_width, sprite_height = sprite.get_size()

        scale_x = block_width / sprite_width
        scale_y = block_height / sprite_height
        scale = min(scale_x, scale_y)  # proportional skalieren (kann angepasst werden)

        scaled_sprite = pygame.transform.smoothscale(sprite, (int(sprite_width * scale), int(sprite_height * scale)))

        overlay = pygame.Surface((block_width, block_height), pygame.SRCALPHA)

        overlay.fill((*base_color, alpha))

        # use the sprite as mask
        sprite_mask = pygame.mask.from_surface(scaled_sprite)
        mask_surface = sprite_mask.to_surface(setcolor=(*base_color, alpha), unsetcolor=(0, 0, 0, 0))

        sprite_pos_x = (block_width - scaled_sprite.get_width()) // 2
        sprite_pos_y = (block_height - scaled_sprite.get_height()) // 2

        overlay.blit(mask_surface, (sprite_pos_x, sprite_pos_y), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(overlay, (screen_x, screen_y))


    def draw_items(self, screen, camera):
        """Draw all items on the grid"""
        for block in self.grid_manager.blocks.values():
            # Check if block is within visible bounds
            if not self._block_is_visible(block, camera):
                continue
            
            # Draw items on the conveyor belt
            if isinstance(block, ConveyorBelt):
                if block.item:
                    block.item.draw(screen, camera)
    

    def draw_conveyor_belts(self, screen, camera):
        """Draw all conveyor belts on the grid"""
        for (tile_x, tile_y), block in self.grid_manager.blocks.items():
            # Check if block is within visible bounds
            if not self._block_is_visible(block, camera):
                continue
            
            # Draw the conveyor belt
            if isinstance(block, ConveyorBelt):
                block.draw(screen, camera)
    