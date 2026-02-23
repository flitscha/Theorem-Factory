import pygame
from machines.menu.elements.tool_tip import Tooltip

class ItemSlot:
    # An item slot (used in machine menus) to display an item. Optionally with a label on the left. (e.g "Input", "Output")
    def __init__(self, rect, label=None, item=None):
        self.rect = rect
        self.label = label
        self.item = item
        self.hovered = False

        self.small_font = pygame.font.SysFont(None, 24)
        self.tooltip = Tooltip(self.small_font)


    def update(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        self.hovered = self.rect.collidepoint(mouse_pos)

        # update Tooltip
        self.tooltip.hide()
        if self.hovered and self.item:
            if self.item.is_theorem:
                lines = ["Theorem: " + str(self.item.formula)]
            else:
                lines = ["Formula: " + str(self.item.formula)]
            if self.item.assumptions:
                lines.append("")
                lines.append("Assumptions:")
                lines.extend([str(a) for a in self.item.assumptions])
            self.tooltip.show(lines, (mouse_pos[0] + 16, mouse_pos[1] + 12))


    def draw_overlay(self, surface):
        self.tooltip.draw(surface)


    def draw_content(self, surface, font, small_font):
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

