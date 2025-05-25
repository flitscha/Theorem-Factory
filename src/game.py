import pygame

from settings import *
from grid import Grid
from camera import Camera

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.grid = Grid()
        self.camera = Camera()

        self.last_mouse_pos = (0, 0) # mouse position, one frame before
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_wheel_dir = 0 # 0 for no scroll, positive for scroll up, negative for scroll down

        self.is_dragging = False


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
        
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            self.last_mouse_pos = self.mouse_pos
            self.mouse_pos = pygame.mouse.get_pos()
            self.camera.update(keys, self.mouse_wheel_dir, self.mouse_pos, self.last_mouse_pos, self.is_dragging)
            self.grid.draw_grid_lines(self.screen, self.camera.offset_x, self.camera.offset_y, self.camera.zoom)

            self.clock.tick(60)
            #print(f"FPS: {self.clock.get_fps():.2f}")
            pygame.display.flip()


        pygame.quit()