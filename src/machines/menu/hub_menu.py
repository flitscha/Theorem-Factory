import pygame

from machines.menu.abstract_menu import AbstractMenu


class HubMenu(AbstractMenu):
    def __init__(self, screen, size, hub_instance):
        super().__init__(screen, size)
        self.hub = hub_instance
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 24)


    def update(self):
        super().update()
        pass

    
    def _draw_item(self, item, count, y):
        start_x = self.rect.x + 20
        string = "Theorem:    " if item.is_theorem else "Formula:    "
        string += str(item.formula)
        string += "       Amount: " + str(count)
        text = self.small_font.render(string, True, (255, 255, 255))
        self.screen.blit(text, (start_x, y))
        y += 25

        if len(item.assumptions) != 0:
            text = self.small_font.render("Assumptions:", True, (255, 255, 255))
            self.screen.blit(text, (start_x + 20, y))
            y += 25

            for assumption in item.assumptions:
                text = self.small_font.render(str(assumption), True, (255, 255, 255))
                self.screen.blit(text, (start_x + 40, y))
                y += 25

        return y + 15


    def draw(self):
        super().draw()

        # title
        title = self.font.render("Hub Inventory", True, (255, 255, 255))
        title_x = self.rect.centerx - title.get_width() // 2
        self.screen.blit(title, (title_x, self.rect.y + 10))

        # draw the items
        # TODO: do this in a table-gui-component
        y = self.rect.y + 50
        storage = self.hub.storage

        for item, count in storage.items():
            y_new = self._draw_item(item, count, y)
            y = y_new

        



