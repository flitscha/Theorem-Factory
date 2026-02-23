from machines.base.machine import Machine
from core.theorem_key import TheoremKey
from entities.item import Item

class Hub(Machine):
    def __init__(self, machine_data, rotation=0):
        super().__init__(machine_data, rotation=rotation)
        self.storage: dict[TheoremKey, int] = {}

    def _to_key(self, item: Item | TheoremKey) -> TheoremKey:
        return item.key if isinstance(item, Item) else item

    def add(self, item: Item | TheoremKey, amount=1):
        key = self._to_key(item)
        self.storage[key] = self.storage.get(key, 0) + amount

    def remove(self, item: Item | TheoremKey, amount=1):
        key = self._to_key(item)
        if key in self.storage:
            self.storage[key] -= amount
            if self.storage[key] <= 0:
                del self.storage[key]

    def items(self):
        return self.storage.items()

    def count(self, item: Item | TheoremKey) -> int:
        key = self._to_key(item)
        return self.storage.get(key, 0)
