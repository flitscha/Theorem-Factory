import pygame
from machines.menu.elements.table_header import TableHeader
from machines.menu.elements.tool_tip import Tooltip

class InventoryTable:
    def __init__(self, rect, font, small_font):
        self.rect = rect
        self.font = font
        self.small_font = small_font

        self.header_height = 40
        self.row_height = 40

        self.header = TableHeader(pygame.Rect(rect.x, rect.y, rect.width, self.header_height), font)

        self.items = [] # list[(TheoremKey, count)]
        self.selected_index: int | None = None

        self.scroll_offset = 0
        self.max_scroll = 0

        self.hovered_index = 0

        self.tooltip = Tooltip(self.small_font)


    # -------------------- data -----------------------
    def set_items(self, storage_dict):
        self.items = list(storage_dict.items())
        self._apply_sort()
        self._recalculate_scroll_bounds()

    def _apply_sort(self):
        if not self.header.sort_key:
            return

        key = self.header.sort_key
        reverse = self.header.sort_reverse

        if key == "formula":
            self.items.sort(
                key=lambda pair: str(pair[0].formula),
                reverse=reverse,
            )

        elif key == "count":
            self.items.sort(
                key=lambda pair: pair[1],
                reverse=reverse,
            )

    def _recalculate_scroll_bounds(self):
        content_height = len(self.items) * self.row_height
        visible_height = self.rect.height - self.header_height
        self.max_scroll = max(0, content_height - visible_height)
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))


    # ---------------- event handling ----------------------
    def handle_events(self, events):
        for event in events:
            # header sorting
            result = self.header.handle_event(event)
            if result:
                self._apply_sort()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(event.pos):
                    continue
                if event.button == 4:  # scroll up
                    self.scroll_offset -= self.row_height
                elif event.button == 5:  # scroll down
                    self.scroll_offset += self.row_height
                elif event.button == 1:
                    self._handle_click(event.pos)

            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    def _handle_click(self, mouse_pos):
        if not self._content_rect().collidepoint(mouse_pos):
            return

        index = self._mouse_to_index(mouse_pos)
        if index is not None:
            self.selected_index = index


    # ------------- update -------------------
    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self._content_rect().collidepoint(mouse_pos):
            self.hovered_index = self._mouse_to_index(mouse_pos)
        else:
            self.hovered_index = None

        self._update_tooltip()

    def _update_tooltip(self):
        if not self.tooltip:
            return

        if self.hovered_index is None:
            self.tooltip.hide()
            return

        key, _ = self.items[self.hovered_index]

        if not key.assumptions:
            self.tooltip.hide()
            return

        lines = ["Assumptions:"]
        for a in key.assumptions:
            lines.append(str(a))

        self.tooltip.show("\n".join(lines))


    # ------------------- Draw -------------------
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        self.header.draw(screen)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        content_rect = self._content_rect()

        # clip drawing to content area
        previous_clip = screen.get_clip()
        screen.set_clip(content_rect)

        for index, (key, count) in enumerate(self.items):
            y = content_rect.y + index * self.row_height - self.scroll_offset

            row_rect = pygame.Rect(content_rect.x+2, y+2, content_rect.width-4, self.row_height-4)

            if not row_rect.colliderect(content_rect):
                continue

            self._draw_row(screen, row_rect, key, count, index)

        screen.set_clip(previous_clip)
        self.tooltip.draw(screen)


    def _draw_row(self, screen, rect, key, count, index):
        if index == self.selected_index:
            pygame.draw.rect(screen, (80, 80, 120), rect)
        elif index == self.hovered_index:
            pygame.draw.rect(screen, (70, 70, 70), rect)

        # shape column
        shape_center = (rect.x + 30, rect.centery)
        self._draw_shape(screen, shape_center, key)

        # formula
        formula_text = self.small_font.render(
            str(key.formula), True, (255, 255, 255)
        )
        screen.blit(formula_text, (rect.x + 80, rect.y + 10))

        # count
        count_text = self.small_font.render(
            str(count), True, (255, 255, 255)
        )
        screen.blit(count_text, (rect.right - 120, rect.y + 10))


    # --------------- Helpers -------------------
    def _draw_shape(self, screen, center, key):
        size = 12

        if not key.is_theorem:
            pygame.draw.circle(screen, (200, 200, 200), center, size)

        elif key.assumptions:
            points = [
                (center[0], center[1] - size),
                (center[0] - size, center[1] + size),
                (center[0] + size, center[1] + size),
            ]
            pygame.draw.polygon(screen, (200, 200, 200), points)

        else:
            rect = pygame.Rect(0, 0, size * 2, size * 2)
            rect.center = center
            pygame.draw.rect(screen, (200, 200, 200), rect)

    def _mouse_to_index(self, mouse_pos):
        content_rect = self._content_rect()

        relative_y = mouse_pos[1] - content_rect.y + self.scroll_offset
        index = relative_y // self.row_height

        if 0 <= index < len(self.items):
            return int(index)

        return None

    def _content_rect(self):
        return pygame.Rect(
            self.rect.x,
            self.rect.y + self.header_height,
            self.rect.width,
            self.rect.height - self.header_height,
        )

