from dataclasses import dataclass
from core.formula import Formula
from core.formula_parser import parse_formula

@dataclass(frozen=True)
class TheoremKey:
    formula: Formula
    assumptions: frozenset[Formula]
    is_theorem: bool


    def to_data(self) -> dict:
        return {
            "formula": str(self.formula),
            "assumptions": [str(a) for a in self.assumptions],
            "is_theorem": self.is_theorem,
        }

    @staticmethod
    def from_data(data: dict) -> "TheoremKey":
        formula = parse_formula(data["formula"])
        assumptions_strings = data.get("assumptions", [])
        assumptions = frozenset(parse_formula(a) for a in assumptions_strings)
        is_theorem = data["is_theorem"]

        return TheoremKey(formula, assumptions, is_theorem)
