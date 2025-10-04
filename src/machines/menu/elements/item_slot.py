import pygame

class ItemSlot:
    # An item slot (used in machine menus) to display an item. Optionally with a label on the left. (e.g "Input", "Output")
    def __init__(self, rect, label=None, item=None):
        self.rect = rect
        self.label = label
        self.item = item
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface, font, small_font):
        # draw border
        pygame.draw.rect(surface, (180, 180, 180), self.rect, 2)

        # label left of slot
        if self.label:
            txt = small_font.render(self.label, True, (200, 200, 200))
            txt_y = self.rect.centery - txt.get_height() // 2
            surface.blit(txt, (self.rect.x - txt.get_width() - 8, txt_y))

        # item inside
        if self.item:
            pygame.draw.rect(surface, (100, 200, 100), self.rect.inflate(-8, -8))
        else:
            empty_txt = small_font.render("–", True, (120, 120, 120))
            surface.blit(empty_txt, (self.rect.centerx - empty_txt.get_width() // 2,
                                     self.rect.centery - empty_txt.get_height() // 2))