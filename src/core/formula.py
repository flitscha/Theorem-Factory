from abc import ABC, abstractmethod

class Formula(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass


class Variable(Formula):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name


class Not(Formula):
    def __init__(self, inner: Formula):
        self.inner = inner

    def __str__(self):
        inner_str = str(self.inner)
        if isinstance(self.inner, BinaryOp):
            inner_str = f"({inner_str})"
        return f"-{inner_str}"

    def __eq__(self, other):
        return isinstance(other, Not) and self.inner == other.inner


class BinaryOp(Formula):
    def __init__(self, op: str, left: Formula, right: Formula):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left)
        right_str = str(self.right)

        if isinstance(self.left, BinaryOp) and self._priority(self.left.op) <= self._priority(self.op):
            left_str = f"({left_str})"
        if isinstance(self.right, BinaryOp) and self._priority(self.right.op) <= self._priority(self.op):
            right_str = f"({right_str})"

        return f"{left_str} {self.op} {right_str}"

    def __eq__(self, other):
        return (
            isinstance(other, BinaryOp) and
            self.op == other.op and
            self.left == other.left and
            self.right == other.right
        )

    def _priority(self, op: str) -> int:
        return {
            '-': 2,
            '*': 1,
            '+': 1,
            '->': 0,
        }.get(op, -1)
