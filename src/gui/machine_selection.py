import pygame

from config.constants import MACHINE_SELECTION_GUI_HEIGHT, ITEM_SELECTION_COLOR, ITEM_SELECTION_ICON_BACKGROUND_COLOR

# the gui-bar at the bottom of the screen, where the player selects the machine, he wants to place.
class MachineSelectionBar:
    def __init__(self, screen, machine_database):
        self.screen = screen
        self.machine_database = machine_database
        self.selected_machine_id = None

        # Visual settings
        self.height = MACHINE_SELECTION_GUI_HEIGHT
        self.margin = 10 # space between icons (in pixels)
        self.icon_size = 64

        # Prepare buttons
        # self.buttons is a list of dictionarys: {"id", "image", "rect"}
        self.buttons = self.generate_buttons()


    def generate_buttons(self):
        buttons = [] # list of dictionarys
        x = self.margin
        y = self.screen.get_height() - self.height + (self.height - self.icon_size) // 2

        # Add empty selection button
        none_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
        buttons.append({
            "id": "None",
            "image": self.make_empty_icon(),  # helper function below
            "rect": none_rect
        })
        x += self.icon_size + self.margin

        # Eraser tool
        eraser_rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
        buttons.append({
            "id": "eraser",
            "image": self.make_eraser_icon(),
            "rect": eraser_rect
        })
        x += self.icon_size + self.margin

        # all other slots: use the database (later we will distinguish between unlocked machines, and not unlocked)
        for machine_id, data in self.machine_database.machines.items():
            rect = pygame.Rect(x, y, self.icon_size, self.icon_size)
            buttons.append({
                "id": machine_id,
                "image": pygame.transform.scale(data.image, (self.icon_size, self.icon_size)),
                "rect": rect
            })
            x += self.icon_size + self.margin

        return buttons


    def make_empty_icon(self):
        surface = pygame.Surface((self.icon_size, self.icon_size))
        surface.fill((50, 50, 50))

        # Draw an X to indicate "None"
        pygame.draw.line(surface, (100, 100, 100), (0, 0), (self.icon_size, self.icon_size), 3)
        pygame.draw.line(surface, (100, 100, 100), (0, self.icon_size), (self.icon_size, 0), 3)

        return surface
    
    def make_eraser_icon(self):
        surface = pygame.Surface((self.icon_size, self.icon_size))
        surface.fill((80, 30, 30))
        return surface

    def draw(self):
        # Background bar
        bar_rect = pygame.Rect(0, self.screen.get_height() - self.height, self.screen.get_width(), self.height)
        pygame.draw.rect(self.screen, ITEM_SELECTION_COLOR, bar_rect)

        # Buttons
        for btn in self.buttons:
            pygame.draw.rect(self.screen, ITEM_SELECTION_ICON_BACKGROUND_COLOR, btn["rect"])
            self.screen.blit(btn["image"], btn["rect"].topleft)

            # Highlight selected
            if btn["id"] == self.selected_machine_id:
                pygame.draw.rect(self.screen, (255, 255, 0), btn["rect"], 2)


    def handle_click(self, mouse_pos):
        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                self.selected_machine_id = btn["id"]
                return btn["id"]
        return None # no icon clicked
    

    def set_tool(self, tool_id):
        self.selected_machine_id = tool_id
