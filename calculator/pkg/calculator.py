class Calculator:
    """
    A class to evaluate simple mathematical expressions.
    This implementation uses two stacks (one for values, one for operators)
    and respects operator precedence.
    """

    def __init__(self):
        """
        Initializes the calculator by defining the available operators
        and their precedence.
        """
        # A dictionary mapping operator symbols to lambda functions that perform the calculation
        self.operators ={
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }
        # A dictionary defining the order of operations.
        # Higher numbers mean higher precedence (e.g., * and / are done before + and -).
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def evaluate(self, expression):
        """
        Method to evaluate a raw string expression.
        
        Args:
            expression (str): The mathematical expression to evaluate (e.g., "3 + 4 * 2")
        
        Returns:
            float: The result of the calculation.
        """
        # 1. Basic input validation
        if not expression or expression.isspace():
            raise ValueError("Expression is empty or whitespace")
        
        # 2. Tokenize the expression.
        # **Note**: This .split() method requires spaces between all numbers and operators.
        # "3 + 4" will work, but "3+4" will fail.
        tokens = expression.strip().split()

        # 3. Call the core evaluation logic
        return self.evaluate_infix(tokens)
    
    def evaluate_infix(self, tokens):
        """
        Core logic to evaluate a list of tokens using a stack-based algorithm.
        
        Args:
            tokens (list): A list of strings, e.g., ["3", "+", "4"]
        
        Returns:
            float: The final calculated result.
        """
        values = [] # A stack to hold numbers (operands)
        operators = [] # A stack to hold operators
        for token in tokens:
            if token in self.operators:
                # The token is an operator.
                # Before adding it, process any operators already on the stack
                # that have *greater than or equal* precedence
                while (operators and
                       operators[-1] in self.operators and
                       self.precedence[operators[-1]] >= self.precedence[token]):
                    # Apply the operator from the top of the stack
                    self.apply_operator(operators, values)
                # Now, push the current, lower-precedence operator onto the stack
                operators.append(token)
            else:
                # The token is not an operator, so assume it's a number.
                try:
                    # Convert it to a float and push it onto the value stack
                    values.append(float(token))
                except ValueError:
                    # Handle invalid tokens (e.g., letters)
                    raise ValueError(f"Invalid token: {token}")
        
        # After the loop, the token list is empty.
        # Apply any remaining operators in the stack.
        while operators:
            self.apply_operator(operators, values)

        # At the end, the value stack should have exactly one item: the final answer.
        if len(values) != 1:
            raise ValueError("Invalid expression")
        
        # Return the final result
        return values[0]

    def apply_operator(self, operators, values):
        """
        A helper function to apply a single operator.
        It pops one operator from the operator stack and two values
        from the value stack, performs the calculation, and pushes the
        result back onto the value stack.
        
        Args:
            operators (list): The stack of operators.
            values (list): The stack of values.
        """

        if len(values) < 2:
            # Not enough operands (e.g., "5 *")
            raise ValueError("Not enough values to apply operator")
        
        # Pop operands in reverse order: b, then a (for "a op b")
        b = values.pop()
        a = values.pop()

        # Pop the operator and find its corresponding function (e.g., lambda a, b: a + b)
        # Perform the calculation and push the result back onto the value stack
        values.append(self.operators[operators.pop()](a,b))