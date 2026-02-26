import pygame


class TableHeader:
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font):
        self.rect = rect
        self.font = font

        # column definitions
        self.columns = [
            {"key": "shape", "label": "", "width": 90, "sortable": False},
            {"key": "formula", "label": "Formula", "width": 500, "sortable": True},
            {"key": "count", "label": "Count", "width": 100, "sortable": True},
        ]

        # sorting state
        self.sort_key = None
        self.sort_reverse = False

        # cached column rects
        self.column_rects: list[pygame.Rect] = []

        self._recalculate_layout()


    def _recalculate_layout(self):
        """Compute the rect for each column."""
        self.column_rects.clear()
        x = self.rect.x + 30

        for col in self.columns:
            col_rect = pygame.Rect(x, self.rect.y, col["width"], self.rect.height)
            self.column_rects.append(col_rect)
            x += col["width"]


    def draw(self, screen):
        # background
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (self.rect.x, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
            2,
        )

        for col, col_rect in zip(self.columns, self.column_rects):
            text = self.font.render(col["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(col_rect.left, col_rect.centery))
            screen.blit(text, text_rect)


    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        for col, col_rect in zip(self.columns, self.column_rects):
            if col_rect.collidepoint(event.pos) and col["sortable"]:
                return self._toggle_sort(col["key"])

        return None


    def _toggle_sort(self, key):
        """Prepare sorting state. Actual sorting is done by table."""
        if self.sort_key == key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key = key
            self.sort_reverse = False

        return {
            "sort_key": self.sort_key,
            "reverse": self.sort_reverse,
        }

