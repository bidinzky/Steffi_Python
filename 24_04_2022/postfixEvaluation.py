def calculate(expr: str) -> int:
    stack: list[int] = []
    tokens = expr.split(" ")
    for token in tokens:
        if token.isnumeric():
            stack.append(int(token))
        elif token in "+-*/":
            right = stack.pop()
            left = stack.pop()
            stack.append(compute(left, token, right))
        elif token == '=':
            return stack.pop()
        else:
            raise ValueError("unknown token {0} found".format(token))


def compute(left: int, op: str, right: int) -> int:
    match op:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return left // right
        case _:
            raise ValueError("op {0} unknown".format(op))
