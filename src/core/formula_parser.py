from core.formula import Formula, Constant, Not, BinaryOp, Variable

OPERATORS = ["->", "+", "*"]
OP_PRIORITY = {"->": 0, "+": 1, "*": 1, "-": 2}

# TODO: understand and test the parser. (because it is AI-generated xD)
def parse_formula(s: str) -> Formula:
    s = s.strip()
    if not s:
        raise ValueError("Empty formula string")

    # 1) constants
    if s == "T":
        return Constant(True)
    elif s == "F":
        return Constant(False)

    # 2) negation
    if s.startswith("-"):
        inner = parse_formula(s[1:])
        return Not(inner)

    # 3) brackets
    if s.startswith("(") and s.endswith(")"):
        depth = 0
        for i, c in enumerate(s):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0 and i < len(s) - 1:
                    break
        else:
            # remove outer bracket
            return parse_formula(s[1:-1])

    # 4) binary operators: split it in 2 formulas (and apply recursion)
    depth = 0
    min_priority = float("inf")
    split_index = -1
    op_found = None

    for i in range(len(s)):
        c = s[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0:
            for op in OPERATORS:
                if s[i:i+len(op)] == op:
                    priority = OP_PRIORITY[op]
                    if priority <= min_priority:
                        min_priority = priority
                        split_index = i
                        op_found = op
                    break

    if split_index != -1 and op_found:
        left = parse_formula(s[:split_index])
        right = parse_formula(s[split_index + len(op_found):])
        return BinaryOp(op_found, left, right)

    # 5) variables
    return Variable(s)