import pygame
import random

from settings import *
from grid import Grid
from camera import Camera
from debug import Debug
from utils import get_mouse_world_pos
from machines.generator import Generator

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.grid = Grid()
        self.camera = Camera()

        self.mouse_wheel_dir = 0 # 0 for no scroll, positive for scroll up, negative for scroll down
        self.is_dragging = False
        self.left_mouse_button_down = False

        self.debug = Debug() # debug overlay


    def handle_events(self):
        self.mouse_wheel_dir = 0  # Reset mouse wheel direction each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # mouse events
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_dir = event.y

            # mouse buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: # right mousebutton down
                    self.is_dragging = True
                elif event.button == 1: # left mousebutton down
                    self.left_mouse_button_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: # right mousebutton up
                    self.is_dragging = False


    def place_machine(self):
        """ If the player clicks on the grid, place a machine at that position. """
        world_x, world_y = get_mouse_world_pos(self.camera)
        
        # calculate the grid position based on world coordinates AND the size of the machine 
        machine_size = (2, 2)  # assuming the machine is 2x2 tiles
        world_x -= (machine_size[0] * TILE_SIZE) / 2
        world_y -= (machine_size[1] * TILE_SIZE) / 2
        grid_x = round(world_x / TILE_SIZE)
        grid_y = round(world_y / TILE_SIZE)

        # Check if the clicked position is empty
        if self.grid.is_empty(grid_x, grid_y, machine_size):
            machine = Generator()
            self.grid.add_block(grid_x, grid_y, machine)


    def run(self):
        
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            self.camera.update(keys, self.mouse_wheel_dir, self.is_dragging)
            self.grid.draw_grid_lines(self.screen, self.camera.offset_x, self.camera.offset_y, self.camera.zoom)
            self.grid.draw_blocks(self.screen, self.camera)

            self.debug.draw(self.screen, self.camera, self.clock)

            if self.left_mouse_button_down:
                self.place_machine()
                self.left_mouse_button_down = False

            self.clock.tick(60)
            pygame.display.flip()


        pygame.quit()