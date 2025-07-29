class SettingsManager:
    def __init__(self):
        # save all settings here
        self._settings = {}

    def register(self, path: str, default_value: bool):
        """register a new setting with a default value. (for example, path could be "debug.show_fps")"""
        if path not in self._settings:
            self._settings[path] = default_value

    def get(self, path: str) -> bool:
        """get the value of a setting"""
        return self._settings.get(path, False)

    def set(self, path: str, value: bool):
        """set the value of a setting"""
        self._settings[path] = value

    def toggle(self, path: str):
        """toggle the value of a setting (True <-> False)."""
        current = self._settings.get(path, False)
        self._settings[path] = not current


# global instance. Import this instance in other files
settings_manager = SettingsManager()

# register the settings
settings_manager.register("debug.show_fps", True)
settings_manager.register("debug.show_coords", False)
settings_manager.register("debug.show_ports", False)