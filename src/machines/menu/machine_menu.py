import pygame
from machines.menu.abstract_menu import AbstractMenu
from machines.menu.elements.tool_tip import Tooltip
from machines.menu.elements.item_slot import ItemSlot

class MachineMenu(AbstractMenu):
    """
    Generic menu for displaying machine info:
    - Title
    - Input slots
    - Output slot
    - Progress bar
    - Previous output
    """
    SLOT_SIZE = 40
    GAP = 10
    BAR_HEIGHT = 14
    PADDING = 20
    OUTPUT_FLASH_FRAMES = 20 # when an item was just produced, show the item in the output slot for these many frames

    def __init__(self, screen, size, machine):
        super().__init__(screen, size)
        self.machine = machine
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 20)
        self.progress = 0.0
        self.title_str = machine.data.name if hasattr(self.machine, "data") else machine.__class__.__name__
        self.input_start_y = self._calculate_input_start_y()
        self.tooltip = Tooltip(self.small_font)

        self._last_seen_prev = self.machine.last_output_item
        self._output_flash_counter = 0

        # list of ItemSlot objects
        self.slots = []
        self._create_slots()
    
    def _calculate_input_start_y(self):
        num_inputs = len(self.machine.input_items)
        total_height = num_inputs * self.SLOT_SIZE + (num_inputs - 1) * self.GAP
        return self.rect.centery - total_height // 2 - 30


    def _create_slots(self):
        """Build slot objects for inputs + output."""
        self.slots.clear()
        # Inputs
        for idx, role in enumerate(self.machine.input_roles):
            rect = pygame.Rect(
                self.rect.x + self.PADDING + 100,
                self.input_start_y + idx * (self.SLOT_SIZE + self.GAP),
                self.SLOT_SIZE, self.SLOT_SIZE
            )
            item = self.machine.input_items[idx] if idx < len(self.machine.input_items) else None
            self.slots.append(ItemSlot(rect, label=role, item=item))

        # Output
        out_x = self.rect.x + self.rect.width - self.PADDING - self.SLOT_SIZE - 100
        out_y = self.input_start_y
        out_rect = pygame.Rect(out_x, out_y, self.SLOT_SIZE, self.SLOT_SIZE)
        self.slots.append(ItemSlot(out_rect, label="output", item=self.machine.output_item))

    
    def update(self):
        super().update()
        self.progress = self.machine.timer / self.machine.processing_duration

        # update slot item references
        for slot in self.slots:
            if slot.label == "output":
                if self.machine.output_item:
                    slot.item = self.machine.output_item
                elif self._output_flash_counter > 0:
                    slot.item = self.machine.last_output_item
                else:
                    slot.item = None
            else:
                idx = self.machine.input_roles.index(slot.label)
                slot.item = self.machine.input_items[idx] if idx < len(self.machine.input_items) else None

        # detect new output
        if self.machine.last_output_item is not self._last_seen_prev:
            self._last_seen_prev = self.machine.last_output_item
            self._output_flash_counter = self.OUTPUT_FLASH_FRAMES
        if self._output_flash_counter > 0:
            self._output_flash_counter -= 1

        # Hover logic for tooltip
        mouse_pos = pygame.mouse.get_pos()
        self.tooltip.hide()
        for slot in self.slots:
            slot.update(mouse_pos)
            if slot.hovered and slot.item:
                if slot.item.is_theorem:
                    lines = ["Theorem: " + str(slot.item.formula)]
                else:
                    lines = ["Formula: " + str(slot.item.formula)]
                if slot.item.assumptions:
                    lines.append("")
                    lines.append("Assumptions:")
                    lines.extend([str(a) for a in slot.item.assumptions])
                self.tooltip.show(lines, (mouse_pos[0] + 16, mouse_pos[1] + 12))
                break

      
    def draw_progress_bar(self, surface, rect, progress):
        """Draw a simple progress bar [0.0 - 1.0]."""
        pygame.draw.rect(surface, (100, 100, 100), rect)
        fill_width = int(rect.width * max(0, min(1, progress)))
        pygame.draw.rect(surface, (80, 180, 250), (rect.x, rect.y, fill_width, rect.height))



    def draw(self):
        super().draw()

        # Title
        title = self.font.render(self.title_str, True, (255, 255, 255))
        title_x = self.rect.centerx - title.get_width() // 2
        self.screen.blit(title, (title_x, self.rect.y + 10))

        # Draw slots
        for slot in self.slots:
            slot.draw(self.screen, self.font, self.small_font)

        # Progress bar
        bar_label = self.small_font.render("progress:", True, (220, 220, 220))
        bar_y = self.rect.bottom - 85
        self.screen.blit(bar_label, (self.rect.x + self.PADDING, bar_y))
        bar_rect = pygame.Rect(
            self.rect.x + self.PADDING + 80,
            bar_y,
            self.rect.width - 2 * self.PADDING - 80,
            self.BAR_HEIGHT
        )
        self.draw_progress_bar(self.screen, bar_rect, self.progress)

        # Prev Output line
        prev_y = self.rect.bottom - 45
        prev_txt = "last produced: "
        item = self.machine.last_output_item

        if item:
            prev_txt += str(item.formula)
            prev_render = self.small_font.render(prev_txt, True, (220, 220, 220))
            prev_rect = prev_render.get_rect(topleft=(self.rect.x + self.PADDING, prev_y))
            hover_rect = prev_rect.inflate(60, 20)
            self.screen.blit(prev_render, prev_rect)

            # Tooltip on hover
            mouse_pos = pygame.mouse.get_pos()
            if hover_rect.collidepoint(mouse_pos) and item.assumptions:
                if item.assumptions:
                    lines = ["Assumptions:"]
                    lines.extend([str(a) for a in item.assumptions])
                self.tooltip.show(lines, (mouse_pos[0] + 16, mouse_pos[1] + 12))
        else:
            prev_render = self.small_font.render(prev_txt + "–", True, (220, 220, 220))
            self.screen.blit(prev_render, (self.rect.x + self.PADDING, prev_y))

        # Tooltip drawn last (on top)
        self.tooltip.draw(self.screen)