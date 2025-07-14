from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    MENU_OPEN = "menu_open"

class GameStateManager:
    """Manages different game states and transitions"""
    
    def __init__(self):
        self.current_state = GameState.PLAYING
        self.active_menu = None
        
    def open_menu(self, menu):
        """Open a menu and change state"""
        self.active_menu = menu
        self.current_state = GameState.MENU_OPEN
        
    def close_menu(self):
        """Close current menu and return to playing"""
        self.active_menu = None
        self.current_state = GameState.PLAYING
        
    def is_menu_open(self):
        """Check if any menu is currently open"""
        return self.current_state == GameState.MENU_OPEN
        
    def is_playing(self):
        """Check if game is in playing state"""
        return self.current_state == GameState.PLAYING