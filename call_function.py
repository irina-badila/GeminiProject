# Import all the actual functions that the AI can call
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from google.genai import types # Import the Google Gemini types library, needed to format the response
from config import WORKING_DIR # Import the secure working directory path from the config file

# --- Configuration ---
# Set the base directory for all file operations.
# This is a crucial security boundary.
working_directory = WORKING_DIR

def call_function(function_call_part, verbose=False):
    """
    Acts as a router or dispatcher.
    
    This function receives a 'function_call_part' (a request from the AI model),
    identifies the requested function by its name, executes the
    corresponding *actual* Python function, and then formats the result
    in a way the AI model can understand.

    Args:
        function_call_part (types.Part): The part of the AI's response
                                         that contains the function call.
        verbose (bool, optional): If True, prints more detailed log messages.

    Returns:
        types.Content: A formatted Content object containing the function's
                       result, ready to be sent back to the AI model.
    """
    
    # --- Logging ---
    if verbose:
        # Print detailed log, including the arguments
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        # Print a simple log
        print(f" - Calling function: {function_call_part.name}")

    # --- Routing ---

    result="" # Initialize an empty result string
    # Check the name of the function the AI wants to call
    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory,**function_call_part.args)
    if function_call_part.name ==  "get_file_content":
        result = get_file_content(working_directory,**function_call_part.args)
    if function_call_part.name == "write_file":
        result = write_file(working_directory,**function_call_part.args)
    if function_call_part.name == "run_python_file":
        result = run_python_file(working_directory,**function_call_part.args)
        print(result)

    # --- Response Formatting ---

    # If 'result' is still empty, it means the function name was not recognized.
    if result == "":
        # Return a formatted error message
        return types.Content(
            role="tool", # This role is "tool" (formerly "function")
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    # If we got a result, return it in the required format
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    # The 'response' must be a JSON-serializable object.
                    response={"result": result},
                )
            ],
        )
