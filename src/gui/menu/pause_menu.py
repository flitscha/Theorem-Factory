import json
import os

from config.constants import *
from gui.elements.button import Button
from gui.menu.settings_menu import SettingsMenu
from gui.menu.abstract_menu import AbstractMenu
from gui.menu.controls_menu import ControlsMenu

class PauseMenu(AbstractMenu):
    """Pause menu overlay - separate from machine menus"""
    
    def __init__(self, screen, game_instance):
        super().__init__(screen, width=800, height=600, on_back=self._resume_game, title="Paused")
        self.game_instance = game_instance

        # Create buttons
        self.buttons = self._create_buttons()

        # Submenus
        self.settings_menu = SettingsMenu(screen, on_back=self.close_submenu)
        self.controls_menu = ControlsMenu(screen, on_back=self.close_submenu)
        

    def _create_buttons(self):
        """Create all menu buttons"""
        buttons = []
        button_width = 250
        button_height = 50
        button_spacing = 60
        start_y = self.menu_y + 120
        
        # Resume button
        resume_rect = (
            self.menu_x + (self.width - button_width) // 2,
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

        # Controls button
        controls_rect = (
            resume_rect[0],
            start_y + button_spacing * 2,
            button_width,
            button_height
        )
        buttons.append(Button(controls_rect, "Controls", self._open_controls, self.font))
        
        # Save button (placeholder)
        save_rect = (
            resume_rect[0],
            start_y + button_spacing * 3,
            button_width,
            button_height
        )
        buttons.append(Button(save_rect, "Save Game", self._save_game, self.font))
        
        # Load button (placeholder)
        load_rect = (
            resume_rect[0],
            start_y + button_spacing * 4,
            button_width,
            button_height
        )
        buttons.append(Button(load_rect, "Load Game", self._load_game, self.font))
        
        # Quit button
        quit_rect = (
            resume_rect[0],
            start_y + button_spacing * 5,
            button_width,
            button_height
        )
        buttons.append(Button(quit_rect, "Quit to Desktop", self._quit_game, self.font))
        
        return buttons
    
    
    def _resume_game(self):
        self.close()
        
    def _open_settings(self):
        self.open_submenu(self.settings_menu)
    
    def _open_controls(self):
        self.open_submenu(self.controls_menu)

    def _save_game(self):
        if not self.game_instance:
            print("No game instance available!")
            return

        # create saves-folder
        os.makedirs("saves", exist_ok=True)
        save_path = os.path.join("saves", "save.json")

        # save the game-state
        try:
            with open(save_path, "w") as f:
                json.dump(self.game_instance.to_data(), f, indent=2)
            print(f"Game successfully saved to {save_path}")
        except Exception as e:
            print(f"Failed to save game: {e}")
        

    def _load_game(self):
        save_path = os.path.join("saves", "save.json")
        if not os.path.exists(save_path):
            print("No save file found!")
            return

        try:
            with open(save_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to load save file: {e}")
            return

        self.game_instance.from_data(data)
        print("Game successfully loaded.")

        
    def _quit_game(self):
        if self.game_instance:
            self.game_instance.running = False
        self.close()