def calculate(expr) :
    stack = []
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


def compute(left, op, right):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return left // right
    else:
        raise ValueError("unknown operator {0} found".format(op))
