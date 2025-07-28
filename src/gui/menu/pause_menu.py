import pygame
from config.settings import *
from gui.elements.button import Button
from gui.menu.settings_menu import SettingsMenu

class PauseMenu:
    """Pause menu overlay - separate from machine menus"""
    
    def __init__(self, screen, game_state_manager, game_instance=None):
        self.screen = screen
        self.game_state = game_state_manager
        self.game_instance = game_instance
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.is_open = False
        
        # Semi-transparent overlay
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))
        
        # Menu dimensions
        self.menu_width = 300
        self.menu_height = 400
        self.menu_x = (SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_height) // 2
        
        # Create buttons
        self.buttons = self._create_buttons()

        # Submenus
        self.settings_menu = SettingsMenu(screen, game_state_manager, on_back=self._close_submenu)
        self.active_submenu = None
        
    def _create_buttons(self):
        """Create all menu buttons"""
        button_width = 200
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 100
        
        buttons = []
        
        # Resume button
        resume_rect = (
            self.menu_x + (self.menu_width - button_width) // 2,
            start_y,
            button_width,
            button_height
        )
        buttons.append(Button(resume_rect, "Resume", self._resume_game, self.font))
        
        # Settings button (placeholder)
        settings_rect = (
            resume_rect[0],
            start_y + button_spacing,
            button_width,
            button_height
        )
        buttons.append(Button(settings_rect, "Settings", self._open_settings, self.font))
        
        # Save button (placeholder)
        save_rect = (
            resume_rect[0],
            start_y + button_spacing * 2,
            button_width,
            button_height
        )
        buttons.append(Button(save_rect, "Save Game", self._save_game, self.font))
        
        # Load button (placeholder)
        load_rect = (
            resume_rect[0],
            start_y + button_spacing * 3,
            button_width,
            button_height
        )
        buttons.append(Button(load_rect, "Load Game", self._load_game, self.font))
        
        # Quit button
        quit_rect = (
            resume_rect[0],
            start_y + button_spacing * 4,
            button_width,
            button_height
        )
        buttons.append(Button(quit_rect, "Quit to Desktop", self._quit_game, self.font))
        
        return buttons
    
    def open(self):
        """Open the pause menu"""
        self.is_open = True
        self.game_state.pause_game()
        
    def close(self):
        """Close the pause menu"""
        self.is_open = False
        self.game_state.resume_game()
    
    def _resume_game(self):
        """Resume the game"""
        self.close()
        
    def _open_settings(self):
        """Open settings menu"""
        self.active_submenu = self.settings_menu
        self.settings_menu.open()
        
    def _save_game(self):
        """Save the game (placeholder)"""
        print("Save game - TODO: Implement")
        # TODO: Implement save functionality
        
    def _load_game(self):
        """Load a game (placeholder)"""
        print("Load game - TODO: Implement")
        # TODO: Implement load functionality
        
    def _quit_game(self):
        """Quit the game"""
        if self.game_instance:
            self.game_instance.running = False
        self.close()
    
    def _close_submenu(self):
        if self.active_submenu:
            self.active_submenu.close()
            self.active_submenu = None

    def handle_events(self, events):
        """Handle input events"""
        if not self.is_open:
            return
        
        # if a submenu is open, the events get tranfered to the submenu
        if self.active_submenu:
            self.active_submenu.handle_events(events)
            return
        
        # resume game, if esc was pressed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._resume_game()
            
        # Forward events to buttons
        for button in self.buttons:
            button.handle_events(events)
    
    def update(self):
        """Update menu state"""
        if not self.is_open:
            return
        if self.active_submenu:
            self.active_submenu.update()
            return
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
    
    def draw(self):
        """Draw the pause menu"""
        if not self.is_open:
            return
            
        # Draw semi-transparent overlay
        self.screen.blit(self.overlay, (0, 0))

        # draw the submenu, if active
        if self.active_submenu:
            self.active_submenu.draw()
            return
        
        # Draw menu background
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(self.screen, (40, 40, 40), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 3)
        
        # Draw title
        title_text = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.menu_x + self.menu_width // 2, self.menu_y + 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        