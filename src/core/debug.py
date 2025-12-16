import pygame

from core.utils import get_mouse_world_pos
from config.constants import TILE_SIZE
from config.settings_manager import settings_manager
from core.performance_tracker import performance_tracker


class Debug():
    def __init__(self):
        self.font = pygame.font.SysFont(None, 16)
        self.text_color = (255, 255, 255)

    # --- Text helper ---
    def _draw_text(self, screen, text, x, y, color=None):
        if color is None:
            color = self.text_color
        surface = self.font.render(text, True, color)
        screen.blit(surface, (x, y))
    
    # --- Coordinates & FPS ---
    def draw_coordinates(self, screen, camera):
        mouse_world_x, mouse_world_y = get_mouse_world_pos(camera)
        tile_x = mouse_world_x // TILE_SIZE
        tile_y = mouse_world_y // TILE_SIZE
        self._draw_text(screen, f"coords: ({tile_x}, {tile_y})", 10, 10)
    

    def draw_fps(self, screen, clock):
        fps = clock.get_fps()
        fps_text = f"FPS: {int(fps)}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        fps_rect = fps_surface.get_rect(topright=(screen.get_width() - 10, 10))
        screen.blit(fps_surface, fps_rect)

    #  performance-tree
    def build_tree(self, flat_data):
        """
        creates a tree, using the flat data provided by the performance_tracker.
        Example: 
        {"update.total", "update.items", "update.machines"}
        creates the tree:

        update.total
            items
            machines
        """
        tree = {}

        # search all parent nodes
        parents = {k: v for k, v in flat_data.items() if k.endswith("total")}
        children = {k: v for k, v in flat_data.items() if not k.endswith("total")}

        for parent_name, t in parents.items():
            node = {"__time__": t}
            # all subnodes for the current parent
            prefix = parent_name.replace(".total", "")
            for child_name, ct in children.items():
                if child_name.startswith(prefix + "."):
                    sub_key = child_name[len(prefix)+1:]
                    node[sub_key] = {"__time__": ct}
            tree[parent_name] = node

        return tree



    def draw_tree(self, screen, tree, x, y, indent=0):
        for key, node in tree.items():
            if key == "__time__":
                continue

            t = node.get("__time__", 0.0)
            self._draw_text(
                screen,
                f"{'  '*indent}{key:12s} {t*1000:6.2f} ms",
                x,
                y
            )
            y += 18

            y0 = self.draw_tree(screen, node, x, y, indent + 2)
            if y0 > y:
                y = y0 + 10
            else:
                y = y0

        return y

    def draw(self, screen, camera, clock):
        if settings_manager.get("debug.show_coords"):
            self.draw_coordinates(screen, camera)

        if settings_manager.get("debug.show_fps"):
            self.draw_fps(screen, clock)
        
        if settings_manager.get("debug.show_performance"):
            tree = self.build_tree(performance_tracker.get_data(smoothed=True))
            self.draw_tree(screen, tree, 10, 60)
        