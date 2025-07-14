import pygame
from typing import List

from entities.port import Port
from core.utils import world_to_screen
from config.settings import TILE_SIZE
from entities.port import Direction

class Machine:
    def __init__(self, size=(1, 1), color=(200, 200, 200), image=None, rotation=0):
        self.size = size # size in grid tiles. Can be changed by rotation
        self.color = color
        self.image = image
        self.rotation = rotation
        self.update_rotated_size()
        self.rotate_image()
        self.origin = None  # will be set on placement

        # port system
        self.ports: List[Port] = []
        self.input_ports: List[Port] = []
        self.output_ports: List[Port] = []

        # initialize ports
        self.init_ports()
        self.rotate_ports()
    
    def init_ports(self):
        """Initialize the ports for this machine. Override in subclasses."""
        pass

    def add_port(self, port: Port):
        """Add a port to this machine"""
        port.machine = self
        self.ports.append(port)
        
        if port.port_type == "input":
            self.input_ports.append(port)
        elif port.port_type == "output":
            self.output_ports.append(port)
    
    def disconnect_all_ports(self):
        """Disconnect all ports of this machine"""
        for port in self.ports:
            port.disconnect()

    def rotate_ports(self):
        direction_rotation = {
            Direction.NORTH: [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST],
            Direction.EAST:  [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH],
            Direction.SOUTH: [Direction.SOUTH, Direction.WEST, Direction.NORTH, Direction.EAST],
            Direction.WEST:  [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH],
        }
        
        for port in self.ports:
            old_x, old_y = port.relative_x, port.relative_y

            # update position
            if self.rotation == 1:
                port.relative_x = self.size[1] - 1 - old_y
                port.relative_y = old_x
            elif self.rotation == 2:
                port.relative_x = self.size[0] - 1 - old_x
                port.relative_y = self.size[1] - 1 - old_y
            elif self.rotation == 3:
                port.relative_x = old_y
                port.relative_y = self.size[0] - 1 - old_x

            # Update direction
            if port.direction:
                port.direction = direction_rotation[port.direction][self.rotation % 4]
            

    def update_rotated_size(self):
        # rotation 0 or 2 means size stays same, 1 or 3 swaps width/height
        if self.rotation % 2 == 1:
            self.size = (self.size[1], self.size[0])

    def rotate_image(self):
        if self.image:
            self.image = pygame.transform.rotate(self.image, -90 * self.rotation)
    
    def update(self):
        pass

    
    def draw(self, screen, camera, grid_x, grid_y):
        screen_x, screen_y = world_to_screen(grid_x * TILE_SIZE, grid_y * TILE_SIZE, camera)

        # draw the image of the machine, if it exists
        if self.image:
            scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.size[0] * TILE_SIZE * camera.zoom), 
                 int(self.size[1] * TILE_SIZE * camera.zoom))
            )
            screen.blit(scaled_image, (screen_x, screen_y))
        
        # otherwise draw a rectangle
        else:
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(screen_x, screen_y, 
                            self.size[0] * TILE_SIZE * camera.zoom, 
                            self.size[1] * TILE_SIZE * camera.zoom)
            )
        # Draw ports for debugging
        self.draw_ports(screen, camera, grid_x, grid_y)
    

    def draw_ports(self, screen, camera, grid_x, grid_y):
        """Draw ports for debugging purposes"""
        for port in self.ports:
            # get a position in between the port-position and the connection position
            port_world_x, port_world_y = port.get_grid_position()
            port_connection_x, port_connection_y = port.get_connection_position()

            x = (1.4 * port_world_x + port_connection_x) / 2.4
            y = (1.4 * port_world_y + port_connection_y) / 2.4
            
            port_world_x, port_world_y = port.get_grid_position()
            port_screen_x, port_screen_y = world_to_screen(
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2,
                camera
            )
            
            # Color based on port type
            color = (0, 255, 0) if port.port_type == "input" else (255, 0, 0)
            
            # Draw port as small circle
            radius = int(4 * camera.zoom)
            pygame.draw.circle(screen, color, (int(port_screen_x), int(port_screen_y)), radius)
            
            # Draw connection indicator
            if port.connected_port:
                pygame.draw.circle(screen, (255, 255, 255), (int(port_screen_x), int(port_screen_y)), radius + 3, 3)

