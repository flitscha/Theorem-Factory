import pygame
from typing import List, Optional

from core.port import Port
from core.utils import world_to_screen
from config.settings import TILE_SIZE

class Machine:
    def __init__(self, size=(1, 1), color=(200, 200, 200), image=None, rotation=0):
        self.base_size = size # size in grid tiles
        self.color = color
        self.image = image
        self.rotation = rotation
        self.rotated_size = None
        self.update_rotated_size()
        self.rotate_image()
        self.origin = None  # will be set on placement

        # port system
        self.ports: List[Port] = []
        self.input_ports: List[Port] = []
        self.output_ports: List[Port] = []

        # initialize ports
        self.init_ports()
    
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
    
    def get_port_at_position(self, grid_x: int, grid_y: int) -> Optional[Port]:
        """Get port at specific grid position"""
        for port in self.ports:
            if port.get_world_position() == (grid_x, grid_y):
                return port
        return None
    
    def check_conveyor_connections(self, grid):
        """Check and update conveyor connections for all ports"""
        for port in self.ports:
            connection_pos = port.get_connection_position()
            block = grid.get_block(connection_pos[0], connection_pos[1])
            
            # Check if there's a conveyor at the connection position
            if block and hasattr(block, 'try_accept_item'):  # It's a conveyor
                # Check if conveyor direction matches port
                if self.is_conveyor_compatible(port, block):
                    port.connected_conveyor = block
                else:
                    port.connected_conveyor = None
            else:
                port.connected_conveyor = None
    
    def is_conveyor_compatible(self, port: Port, conveyor) -> bool:
        """Check if conveyor direction is compatible with port"""
        if port.port_type == "output":
            # Output port: conveyor should accept items from this direction
            conveyor_input_pos = conveyor.get_input_position()
            return conveyor_input_pos == port.get_world_position()
        else:
            # Input port: conveyor should output items to this direction
            conveyor_output_pos = conveyor.get_output_position()
            return conveyor_output_pos == port.get_world_position()

    def update_rotated_size(self):
        # rotation 0 or 2 means size stays same, 1 or 3 swaps width/height
        if self.rotation % 2 == 1:
            self.rotated_size = (self.base_size[1], self.base_size[0])
        else:
            self.rotated_size = self.base_size

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
                (int(self.rotated_size[0] * TILE_SIZE * camera.zoom), 
                 int(self.rotated_size[1] * TILE_SIZE * camera.zoom))
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
            port_world_x, port_world_y = port.get_world_position()
            port_screen_x, port_screen_y = world_to_screen(
                port_world_x * TILE_SIZE + TILE_SIZE // 2,
                port_world_y * TILE_SIZE + TILE_SIZE // 2,
                camera
            )
            
            # Color based on port type
            color = (0, 255, 0) if port.port_type == "input" else (255, 0, 0)
            
            # Draw port as small circle
            radius = max(3, int(8 * camera.zoom))
            pygame.draw.circle(screen, color, (int(port_screen_x), int(port_screen_y)), radius)
            
            # Draw connection indicator
            if port.connected_conveyor:
                pygame.draw.circle(screen, (255, 255, 255), (int(port_screen_x), int(port_screen_y)), radius + 2, 2)

