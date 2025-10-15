class Calculator:
    def __init__(self):
        self.operators ={
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            raise ValueError("Expression is empty or whitespace")
        tokens = expression.strip().split()
        return self.evaluate_infix(tokens)
    
    def evaluate_infix(self, tokens):
        values = []
        operators = []
        for token in tokens:
            if token in self.operators:
                while (operators and
                       operators[-1] in self.operators and
                       self.precedence[operators[-1]] >= self.precedence[token]):
                    self.apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
        while operators:
            self.apply_operator(operators, values)
        if len(values) != 1:
            raise ValueError("Invalid expression")
        return values[0]
    def apply_operator(self, operators, values):
        if len(values) < 2:
            raise ValueError("Not enough values to apply operator")
        b = values.pop()
        a = values.pop()
        values.append(self.operators[operators.pop()](a,b))