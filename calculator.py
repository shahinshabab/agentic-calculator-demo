import ast
import operator


class CalculatorError(ValueError):
    pass


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> float:
    expression = expression.strip()
    if not expression or len(expression) > 100:
        raise CalculatorError("Enter an expression up to 100 characters.")
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        raise CalculatorError("That expression cannot be calculated.") from error
    if abs(float(result)) > 1_000_000_000_000:
        raise CalculatorError("The result is outside the demo limit.")
    return float(result)


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.USub, ast.UAdd):
        return OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise CalculatorError("Exponents are limited to 10.")
        return OPERATORS[type(node.op)](left, right)
    raise CalculatorError("Only arithmetic expressions are allowed.")

