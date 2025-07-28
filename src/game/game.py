import pygame
from config.settings import *
from grid.grid_coordinator import GridCoordinator
from core.camera import Camera
from core.debug import Debug
from core.input_handler import InputHandler
from core.renderer import Renderer
from game.game_state import GameState, GameStateManager
from game.machine_manager import MachineManager
from game.input_processor import InputProcessor
from gui.placement_preview import PlacementPreview
from machines.base.machine_database import database as machine_data
from gui.machine_selection import MachineSelectionBar
from gui.menu.pause_menu import PauseMenu

class Game:
    """Main game class that coordinates all systems"""
    
    def __init__(self):
        self._initialize_pygame()
        self._initialize_core_systems()
        self._initialize_game_systems()
        self._initialize_gui()
        
    def _initialize_pygame(self):
        """Initialize pygame and create main window"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        
    def _initialize_core_systems(self):
        """Initialize core game systems"""
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)
        self.camera = Camera()
        self.debug = Debug()
        
    def _initialize_game_systems(self):
        """Initialize game-specific systems"""
        self.grid = GridCoordinator()
        self.game_state = GameStateManager()
        
        # Load machine images
        for machine in machine_data.machines.values():
            machine.load_image()
            
    def _initialize_gui(self):
        """Initialize GUI components"""
        self.placement_preview = PlacementPreview(self.screen, self.grid, self.camera, machine_data)
        self.machine_selection_bar = MachineSelectionBar(self.screen, machine_data)
        
        # Initialize pause menu
        self.pause_menu = PauseMenu(self.screen, self.game_state, self)
        
        # Initialize managers that depend on GUI
        self.machine_manager = MachineManager(
            self.grid, self.camera, self.placement_preview, machine_data
        )
        
        self.input_processor = InputProcessor(
            self.input_handler, self.placement_preview, self.machine_selection_bar,
            self.machine_manager, self.game_state
        )
        
    def update(self, dt):
        """Update all game systems"""
        # Update pause menu
        self.pause_menu.update()

        # Update camera
        if self.game_state.should_update_game():
            keys = pygame.key.get_pressed()
            is_dragging = self.input_handler.is_key_held('mouse_3')
            self.camera.update(keys, self.input_handler.mouse_wheel_dir, is_dragging)
        
            # Update grid
            self.grid.update(dt)
        
        # Update active menu if open
        if self.game_state.is_menu_open() and self.game_state.active_menu:
            self.game_state.active_menu.update()
            

    def render(self):
        """Render the complete frame"""
        self.renderer.clear_screen(BACKGROUND_COLOR)
        
        # Render game world
        self.renderer.render_game_world(self.grid, self.camera)
        
        # Select gui components, based on the game-state
        gui_components = []
        match self.game_state.current_state:
            case GameState.PLAYING:
                gui_components = [self.placement_preview, self.machine_selection_bar]
            case GameState.MENU_OPEN:
                gui_components = [self.game_state.active_menu, self.machine_selection_bar]
            case GameState.PAUSED:
                gui_components = [self.machine_selection_bar, self.pause_menu]

        # render the gui components
        self.renderer.render_gui_components(gui_components)
        
        # Render debug overlay
        self.renderer.render_debug_info(self.debug, self.camera, self.clock)
        
        # Present frame
        self.renderer.present()
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle input
            events = pygame.event.get()
            self.input_handler.update(events)

            # Handle pause menu events
            for event in events:
                self.pause_menu.handle_event(event)
            
            # Process input events
            result = self.input_processor.process_input(self.screen, events, pause_menu=self.pause_menu)
            if result.get("quit"):
                self.running = False
                
            # Update game state
            dt = self.clock.tick(60) / 1000.0
            self.update(dt)
            
            # Render frame
            self.render()
            
        pygame.quit()