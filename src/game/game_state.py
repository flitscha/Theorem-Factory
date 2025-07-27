from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    PAUSED = "paused" # game paused: pause-menu is open
    MENU_OPEN = "menu_open" # machine menus

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
    
    def pause_game(self):
        """Pause the game"""
        if self.current_state == GameState.PLAYING:
            self.current_state = GameState.PAUSED
            
    def resume_game(self):
        """Resume the game from pause"""
        if self.current_state == GameState.PAUSED:
            self.current_state = GameState.PLAYING
            
    def toggle_pause(self):
        """Toggle between paused and playing"""
        if self.current_state == GameState.PLAYING:
            self.pause_game()
        elif self.current_state == GameState.PAUSED:
            self.resume_game()
    
    def is_menu_open(self):
        """Check if any menu is currently open"""
        return self.current_state == GameState.MENU_OPEN
    
    def is_playing(self):
        """Check if game is in playing state"""
        return self.current_state == GameState.PLAYING
        
    def is_paused(self):
        """Check if game is paused"""
        return self.current_state == GameState.PAUSED
        
    def should_update_game(self):
        """Check if game logic should update (not paused)"""
        return self.current_state != GameState.PAUSED

    def should_handle_game_input(self):
        """Check if game input should be processed (not in machine menu)"""
        return self.current_state != GameState.PAUSED