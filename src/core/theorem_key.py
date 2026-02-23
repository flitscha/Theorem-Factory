from dataclasses import dataclass
from core.formula import Formula

@dataclass(frozen=True)
class TheoremKey:
    formula: Formula
    assumptions: frozenset[Formula]
    is_theorem: bool
