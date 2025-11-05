import sys # Import the 'sys' module to access command-line arguments

from pkg.calculator import Calculator # Import the Calculator class from the local 'pkg' package
from pkg.render import format_json_output # Import the JSON formatting function from the local 'pkg' package

def main():
    """
    Main function to run the command-line calculator.
    """

    # Create an instance of the Calculator
    calc = Calculator()

    # Check if the user provided any arguments (sys.argv[0] is always the script name)
    if len(sys.argv) <= 1:
        # If no expression is given, print the usage instructions and exit
        print("Calculator App")
        print("Usage: python main.py '<expression>'")
        print("Example: python main.py '3 + 5'")
        return
    
    # Join all command-line arguments after the script name into a single string.
    # This allows the user to type 'python main.py 3 + 5'
    # which becomes the string "3 + 5".
    expression = " ".join(sys.argv[1:])
    
    # Use a try...except block to handle any errors
    # from the evaluation (like invalid tokens or division by zero).
    try:
        # Evaluate the user's expression
        result = calc.evaluate(expression)

        # The 'evaluate' method raises an error on failure, so if we get here,
        # 'result' should contain a valid number.
        if result is not None:
            # Format the original expression and the result into a "pretty" JSON string
            to_print= format_json_output(expression,result)
            # Print the final JSON to the console
            print(to_print)
        else:
            # Note: This block might be unreachable if 'calc.evaluate'
            # always raises an error for empty/invalid input instead of returning None.
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        # If any error occurred (e.g., ValueError from calculator), catch it.
        # Print the error message in a user-friendly way.
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
