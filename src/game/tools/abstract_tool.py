class AbstractTool:
    """Abstract base for tools (placement, eraser, etc.)"""

    def __init__(self, machine_manager, placement_preview, machine_selection_bar, game_state):
        self.machine_manager = machine_manager
        self.placement_preview = placement_preview
        self.machine_selection_bar = machine_selection_bar
        self.game_state = game_state

    def handle_events(self, events, input_handler, screen):
        """Process raw events (mouse/keyboard)"""
        pass

    def update(self, input_handler):
        """Continuous updates (e.g., while holding mouse button)"""
        pass

    def on_select(self):
        """Called when this tool becomes active"""
        pass

    def on_deselect(self):
        """Called when this tool is deactivated"""
        pass