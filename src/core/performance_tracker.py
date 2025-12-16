import time
from collections import defaultdict


class PerformanceTracker:
    def __init__(self, smoothing=0.99):
        self.sections = {}
        self.current_frame = defaultdict(float)
        self.last_frame = {}
        self.smoothed = {}
        self.smoothing = smoothing

    def start(self, name):
        self.sections[name] = time.perf_counter()

    def end(self, name):
        start = self.sections.get(name)
        if start is not None:
            self.current_frame[name] += time.perf_counter() - start

    def end_frame(self):
        self.last_frame = dict(self.current_frame)

        for name, t in self.last_frame.items():
            prev = self.smoothed.get(name, t)
            self.smoothed[name] = (
                self.smoothing * prev + (1 - self.smoothing) * t
            )

        self.current_frame.clear()

    def get_data(self, smoothed=True):
        return self.smoothed if smoothed else self.last_frame


# global singleton instance
performance_tracker = PerformanceTracker()