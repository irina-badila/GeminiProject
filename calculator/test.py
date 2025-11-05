import unittest #Import the 'unittest' library, Python's built-in testing framework
from pkg.calculator import Calculator # Import the Calculator class that we intend to test

# Define a new test case class that inherits from 'unittest.TestCase'
class TestCalculator(unittest.TestCase):
    def setUp(self):
        """
        The setUp method is a special method run *before* every single test
        (e.g., before test_addition, then again before test_subtraction, etc.).
        This ensures each test gets a fresh, clean instance of the calculator.
        """
        self.calculator = Calculator()

    # --- Testing correct functionality ---
    
    def test_addition(self):
        """Test a simple addition operation."""
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        """Test a simple subtraction operation."""
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        """Test a simple multiplication operation."""
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        """Test a simple division operation."""
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    # --- Operator Precedence Tests ---

    def test_nested_expression(self):
        """Test operator precedence (multiplication before addition)."""
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        """Test a more complex expression with multiple operators."""
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        """Test that an empty string raises a ValueError."""
        # The test PASSES if the code inside this block *raises* a ValueError.
        # It FAILS if it does not.
        with self.assertRaises(ValueError):
            self.calculator.evaluate("")

    def test_invalid_operator(self):
        """Test that an invalid token (not a number or known operator) raises a ValueError."""
        # The calculator implementation should treat '$' as an invalid token.
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        """Test an expression that doesn't have enough values for its operators."""
        # This should fail when 'apply_operator' tries to pop two values but only finds one.
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

if __name__ == "__main__":
    unittest.main()
