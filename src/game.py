import pygame

from settings import *
from grid import Grid

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.grid = Grid()
        self.camera_offset = [0, 0]

    
    def run(self):
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))

            self.grid.draw_grid_lines(self.screen, self.camera_offset)
            pygame.display.flip()


        pygame.quit()