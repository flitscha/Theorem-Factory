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

    
    def run(self):
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            self.camera.update(keys)

            self.grid.draw_grid_lines(self.screen, self.camera.offset_x, self.camera.offset_y)

            self.clock.tick(60)
            #print(f"FPS: {self.clock.get_fps():.2f}")
            pygame.display.flip()


        pygame.quit()