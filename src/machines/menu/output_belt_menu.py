import pygame
from machines.menu.abstract_menu import AbstractMenu
from machines.menu.elements.inventory_table import InventoryTable
from gui.elements.button import Button

class OutputBeltMenu(AbstractMenu):
    def __init__(self, screen, size, machine_instance, hub_instance):
        super().__init__(screen, size)
        self.belt = machine_instance
        self.hub = hub_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 24)

        # table
        table_rect = pygame.Rect(
            self.rect.x + 40,
            self.rect.y + 70,
            self.rect.width - 80,
            self.rect.height - 200,
        )
        self.table = InventoryTable(table_rect, self.font, self.small_font)

        # -------- buttons ----------
        button_y = self.rect.bottom - 80

        self.set_button = Button(
            rect=(self.rect.x + 40, button_y, 160, 40),
            text="Set Filter",
            callback=self._apply_selected_filter,
            font=self.small_font,
        )

        self.clear_button = Button(
            rect=(self.rect.x + 220, button_y, 160, 40),
            text="Clear Filter",
            callback=self._clear_filter,
            font=self.small_font,
        )


    def handle_events(self, events):
        super().handle_events(events)
        self.table.handle_events(events)
        self.set_button.handle_events(events)
        self.clear_button.handle_events(events)


    def _apply_selected_filter(self):
        if self.table.selected_index is None:
            return

        key, _ = self.table.items[self.table.selected_index]
        self.belt.set_filter(key)

    def _clear_filter(self):
        self.belt.set_filter(None)


    def update(self):
        super().update()
        # ensure filter stays visible even if count == 0
        items = dict(self.hub.storage)

        if self.belt.output_filter and self.belt.output_filter not in items:
            items[self.belt.output_filter] = 0

        self.table.set_items(items)
        self.table.update()

        # button state
        self.set_button.set_disabled(True)

        # activate only, if something is selected
        if self.table.selected_index is not None:
            self.set_button.set_disabled(False)

        self.set_button.update()
        self.clear_button.update()

    

    def draw(self):
        super().draw()

        # title
        title = self.font.render("Select output filter", True, (255, 255, 255))
        title_x = self.rect.centerx - title.get_width() // 2
        self.screen.blit(title, (title_x, self.rect.y + 15))

        self.table.draw(self.screen)

        # active filter display
        filter_text = "None"
        if self.belt.output_filter:
            filter_text = str(self.belt.output_filter.formula)

        label = self.small_font.render(
            f"Active filter: {filter_text}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(label, (self.rect.x + 40, self.rect.bottom - 115))

        # buttons
        self.set_button.draw(self.screen)
        self.clear_button.draw(self.screen)

