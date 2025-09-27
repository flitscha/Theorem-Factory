import pygame
from machines.menu.abstract_menu import AbstractMenu

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

        self._last_seen_prev = None
        self._output_flash_counter = 0
    
    def _calculate_input_start_y(self):
        num_inputs = len(self.machine.input_items)
        total_height = num_inputs * self.SLOT_SIZE + (num_inputs - 1) * self.GAP
        return self.rect.centery - total_height // 2 - 30

    def update(self):
        super().update()

        self.progress = self.machine.timer / self.machine.processing_duration

        # check, if a new item was produced
        if self.machine.last_output_item is not self._last_seen_prev:
            self._last_seen_prev = self.machine.last_output_item
            self._output_flash_counter = self.OUTPUT_FLASH_FRAMES

        if self._output_flash_counter > 0:
            self._output_flash_counter -= 1


    def draw_slot(self, surface, rect, item, label=None):
        """Draw one input/output slot with optional label on the left."""
        pygame.draw.rect(surface, (180, 180, 180), rect, 2)

        if label:
            txt = self.small_font.render(label, True, (200, 200, 200))
            txt_y = rect.centery - txt.get_height() // 2
            surface.blit(txt, (rect.x - txt.get_width() - 8, txt_y))

        if item:
            # Placeholder: filled rect
            pygame.draw.rect(surface, (100, 200, 100), rect.inflate(-8, -8))
        else:
            empty_txt = self.small_font.render("–", True, (120, 120, 120))
            surface.blit(empty_txt, (rect.centerx - empty_txt.get_width() // 2,
                                     rect.centery - empty_txt.get_height() // 2))


    def draw_progress_bar(self, surface, rect, progress):
        """Draw a simple progress bar [0.0 - 1.0]."""
        # background
        pygame.draw.rect(surface, (100, 100, 100), rect)
        # filling
        fill_width = int(rect.width * max(0, min(1, progress)))
        pygame.draw.rect(surface, (80, 180, 250), (rect.x, rect.y, fill_width, rect.height))


    def draw(self):
        super().draw()

        title = self.font.render(self.title_str, True, (255, 255, 255))
        title_x = self.rect.centerx - title.get_width() // 2
        self.screen.blit(title, (title_x, self.rect.y + 10))

        # Inputs
        for idx, role in enumerate(self.machine.input_roles):
            rect = pygame.Rect(
                self.rect.x + self.PADDING + 100,
                self.input_start_y + idx * (self.SLOT_SIZE + self.GAP),
                self.SLOT_SIZE, self.SLOT_SIZE
            )
            item = self.machine.input_items[idx] if idx < len(self.machine.input_items) else None
            self.draw_slot(self.screen, rect, item, label=role)

        # Output
        out_x = self.rect.x + self.rect.width - self.PADDING - self.SLOT_SIZE - 100
        out_y = self.input_start_y
        out_rect = pygame.Rect(out_x, out_y, self.SLOT_SIZE, self.SLOT_SIZE)

        # draw normal item or flash last output item
        if self.machine.output_item:
            item_to_draw = self.machine.output_item
        elif self._output_flash_counter > 0:
            item_to_draw = self.machine.last_output_item
        else:
            item_to_draw = None

        self.draw_slot(self.screen, out_rect, item_to_draw, label="Output")

        # Progress Bar
        bar_label = self.small_font.render("progress:", True, (220, 220, 220))
        bar_y = self.rect.bottom - 85
        self.screen.blit(bar_label, (self.rect.x + self.PADDING, bar_y))

        bar_rect = pygame.Rect(self.rect.x + self.PADDING + 80,
                               bar_y,
                               self.rect.width - 2 * self.PADDING - 80,
                               self.BAR_HEIGHT)
        self.draw_progress_bar(self.screen, bar_rect, self.progress)


        # Prev Output
        prev_y = self.rect.bottom - 45
        prev_txt = "Zuletzt produziert: "
        if self.machine.last_output_item:
            prev_txt += str(self.machine.last_output_item.formula)
        else:
            prev_txt += "–"
        prev_render = self.small_font.render(prev_txt, True, (220, 220, 220))
        self.screen.blit(prev_render, (self.rect.x + self.PADDING, prev_y))

