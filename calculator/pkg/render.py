import json # Import the built-in json library for JSON serialization

def format_json_output(expression:str, result:float, indent: int=2) -> str:
    """
    Formats the expression and its result into a "pretty-printed" JSON string.

    Args:
        expression (str): The original mathematical expression.
        result (float): The calculated result.
        indent (int, optional): The number of spaces to use for indentation in the JSON. Defaults to 2.

    Returns:
        str: A JSON-formatted string.
    """

    # Check if the result is a float that represents a whole number (e.g., 5.0)
    if isinstance(result, float) and result.is_integer():
        # If so, convert it to an integer (e.g., 5) for cleaner JSON output
        result_to_dump = int(result)
    else:
        # Otherwise, keep it as a float (e.g., 5.5)
        result_to_dump = result
    
    # Create a Python dictionary to hold the structured data
    output = {
        "expression": expression,
        "result": result_to_dump
    }

    # Convert (serialize) the dictionary into a JSON formatted string
    # 'indent=indent' makes the JSON "pretty-printed" and easier to read
    return json.dumps(output, indent=indent)
