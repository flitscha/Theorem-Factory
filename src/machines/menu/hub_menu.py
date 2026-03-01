import pygame

from machines.menu.abstract_menu import AbstractMenu
from machines.menu.elements.inventory_table import InventoryTable


class HubMenu(AbstractMenu):
    def __init__(self, screen, size, hub_instance):
        super().__init__(screen, size)
        self.hub = hub_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 24)

        table_rect = pygame.Rect(
            self.rect.x + 40,
            self.rect.y + 70,
            self.rect.width - 80,
            self.rect.height - 100,
        )
        self.table = InventoryTable(table_rect, self.font, self.small_font)


    def handle_events(self, events):
        super().handle_events(events)
        self.table.handle_events(events)

    def update(self):
        super().update()
        self.table.set_items(self.hub.storage)
        self.table.update()
    

    def draw(self):
        super().draw()

        # title
        title = self.font.render("Hub Inventory", True, (255, 255, 255))
        title_x = self.rect.centerx - title.get_width() // 2
        self.screen.blit(title, (title_x, self.rect.y + 15))

        self.table.draw(self.screen)

        



