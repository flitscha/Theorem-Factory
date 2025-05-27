import pygame
import random

from settings import *
from grid import Grid
from camera import Camera
from debug import Debug
from machines.machine import Machine

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

        self.debug = Debug() # debug overlay


    def handle_events(self):
        self.mouse_wheel_dir = 0  # Reset mouse wheel direction each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # mouse events
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_dir = event.y

            # right mousebutton
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.is_dragging = False
    

    def run(self):
        machine = Machine()
        self.grid.add_block(0, 0, machine)

        for i in range(100):
            machine = Machine(TILE_SIZE, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.grid.add_block(random.randint(-100, 100), random.randint(-100, 100), machine)
            
        
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            self.camera.update(keys, self.mouse_wheel_dir, self.is_dragging)
            self.grid.draw_grid_lines(self.screen, self.camera.offset_x, self.camera.offset_y, self.camera.zoom)
            self.grid.draw_blocks(self.screen, self.camera)

            self.debug.draw(self.screen, self.camera, self.clock)

            self.clock.tick(60)
            pygame.display.flip()


        pygame.quit()