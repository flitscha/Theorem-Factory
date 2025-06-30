import pygame

from settings import *
from grid import Grid
from camera import Camera
from debug import Debug
from utils import get_mouse_world_pos, get_grid_coordinates_when_placing_machine
from machines.generator import Generator
from grid_highlighter import GridHighlighter
from machine_data import database as machine_data

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        # load machine images
        for machine in machine_data.machines.values():
            machine.load_image()
        
        self.grid = Grid()
        self.camera = Camera()

        self.mouse_wheel_dir = 0 # 0 for no scroll, positive for scroll up, negative for scroll down
        self.is_dragging = False
        self.left_mouse_button_down = False
        self.middle_mouse_button_down = False

        self.debug = Debug() # debug overlay

        self.grid_highlighter = GridHighlighter(self.screen, self.grid, self.camera, machine_data)
        self.grid_highlighter.start_preview("generator")  # Start previewing the generator machine


    def handle_events(self):
        self.mouse_wheel_dir = 0  # Reset mouse wheel direction each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.grid_highlighter.rotate_preview()

            # mouse events
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_dir = event.y

            # mouse buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: # right mousebutton down
                    self.is_dragging = True
                elif event.button == 1: # left mousebutton down
                    self.left_mouse_button_down = True
                elif event.button == 2:  # middle mousebutton down for testing removal
                    self.middle_mouse_button_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: # right mousebutton up
                    self.is_dragging = False


    def place_machine(self):
        """ If the player clicks on the grid, place a machine at that position. """

        # Get the machine ID and rotation from the grid_highlighter
        machine_id = self.grid_highlighter.active_preview
        rotation = self.grid_highlighter.rotation

        if not machine_id:
            return

        # Get machine data
        data = self.grid_highlighter.machine_database.get(machine_id)
        size = data.size

        # Calculate rotated size based on rotation (swap width and height for odd rotations)
        if rotation % 2 == 1:
            rotated_size = (size[1], size[0])
        else:
            rotated_size = size

        # calculate the grid position based on world coordinates AND the size of the machine 
        grid_x, grid_y = get_grid_coordinates_when_placing_machine(self.camera, rotated_size)

        # Check if the clicked position is empty
        if self.grid.is_empty(grid_x, grid_y, rotated_size):
            machine = Generator(machine_data, rotation=rotation)
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

            # testing, to place blocks
            if self.left_mouse_button_down:
                self.place_machine()
                self.left_mouse_button_down = False

            # testing, to delete blocks
            # Remove block on middle mouse click
            if self.middle_mouse_button_down:
                # Get mouse world position and convert to grid coords
                mouse_world_x, mouse_world_y = get_mouse_world_pos(self.camera)
                grid_x = int(mouse_world_x // TILE_SIZE)
                grid_y = int(mouse_world_y // TILE_SIZE)

                self.grid.remove_block(grid_x, grid_y)
                self.middle_mouse_button_down = False


            self.grid_highlighter.draw()

            self.clock.tick(60)
            pygame.display.flip()


        pygame.quit()