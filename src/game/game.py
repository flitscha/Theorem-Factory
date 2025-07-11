import pygame

from config.settings import *
from grid.grid_coordinator import GridCoordinator
from core.camera import Camera
from core.debug import Debug
from core.utils import get_mouse_world_pos, get_grid_coordinates_when_placing_machine, get_mouse_grid_pos
from gui.placement_preview import PlacementPreview
from machines.base.machine_database import database as machine_data
from gui.machine_selection import MachineSelectionBar
from machines.menu.generator_menu import GeneratorMenu
from machines.types.generator import Generator

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
        
        self.grid = GridCoordinator()
        self.camera = Camera()

        self.mouse_wheel_dir = 0 # 0 for no scroll, positive for scroll up, negative for scroll down
        self.is_dragging = False
        self.left_mouse_button_down = False
        self.middle_mouse_button_down = False

        self.debug = Debug() # debug overlay

        self.placement_preview = PlacementPreview(self.screen, self.grid, self.camera, machine_data)

        self.machine_selection_bar = MachineSelectionBar(self.screen, machine_data)

        self.active_menu = None


    def handle_events(self):
        self.mouse_wheel_dir = 0  # Reset mouse wheel direction each frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.placement_preview.rotate_preview()

            # mouse events
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_dir = event.y

            # mouse buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.active_menu:
                    # Forward event to menu
                    self.active_menu.handle_event(event)
                    if self.active_menu.closed:
                        self.active_menu = None
                    continue

                if event.button == 3: # right mousebutton down
                    self.is_dragging = True
                elif event.button == 1: # left mousebutton down
                    self.left_mouse_button_down = True
                    # update the selected machine (using the machine_selection_bar GUI)
                    selected = self.machine_selection_bar.handle_click(event.pos)
                    if selected != "MISS":
                        self.placement_preview.start_preview(selected)
                elif event.button == 2:  # middle mousebutton down for testing removal
                    self.middle_mouse_button_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: # right mousebutton up
                    self.is_dragging = False


    def place_machine(self):
        """ If the player clicks on the grid, place a machine at that position. """

        if pygame.mouse.get_pos()[1] > SCREEN_HEIGHT - MACHINE_SELECTION_GUI_HEIGHT:
            return

        # Get the machine ID and rotation from the placement_preview
        machine_id = self.placement_preview.active_preview
        rotation = self.placement_preview.rotation

        if not machine_id:
            return

        # Get machine data
        data = self.placement_preview.machine_database.get(machine_id)
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
            machine = data.cls(data, rotation=rotation)
            #machine = Generator(machine_data, rotation=rotation)
            self.grid.add_block(grid_x, grid_y, machine)


    def open_machine_menu(self):
        if self.placement_preview.active_preview:
            return
        
        grid_x, grid_y = get_mouse_grid_pos(self.camera)
        block = self.grid.get_block(grid_x, grid_y)
        if block:
            # Open menu for this machine
            if isinstance(block, Generator): # TODO: improve this
                self.active_menu = GeneratorMenu(self.screen, (500, 300), block)


    def run(self):
        
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            dt = self.clock.tick(60) / 1000.0
            self.camera.update(keys, self.mouse_wheel_dir, self.is_dragging)
            self.grid.update(dt)
            self.grid.draw_grid_lines(self.screen, self.camera)
            self.grid.draw_blocks(self.screen, self.camera)

            self.debug.draw(self.screen, self.camera, self.clock)

            # testing, to place blocks
            if self.left_mouse_button_down:
                self.place_machine()
                self.open_machine_menu()
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


            self.placement_preview.draw()

            # GUI elements
            self.machine_selection_bar.draw()
            if self.active_menu:
                self.active_menu.draw()

            # set fps and change frame
            self.clock.tick(60)
            pygame.display.flip()


        pygame.quit()