import os # Import the 'os' module for interacting with the operating system
from google.genai import types # Import the 'types' from the Google Gemini library to define the function schema

def get_files_info(working_directory: str, directory="."):
    """
    Lists the contents (files and directories) of a specified directory.
    
    Performs security checks to ensure the listing is confined to the
    'working_directory'. Returns a formatted string of file names,
    sizes, and whether they are directories.

    Args:
        working_directory (str): The base directory where operations are allowed.
        directory (str, optional): The subdirectory to list. Defaults to "." (the working_directory itself).

    Returns:
        str: A multi-line string listing file info or an error message.
    """
    
    # --- Security & Path Validation ---
    
    # Get the full, absolute path of the allowed working directory
    abs_working_directory=os.path.abspath(working_directory)

    # Get the full, absolute path of the directory the user *wants* to list
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    # **Critical Security Check**:
    # Ensure the requested directory's path *starts with* the working directory's path.
    # This prevents directory traversal attacks (e.g., listing "../").
    if not abs_directory.startswith(abs_working_directory):
        return f"Error: Cannot list '{directory}': directory as it is outside the working directory"
    
    # --- Directory Listing ---

    final_response="";# Initialize an empty string to build the response

    # Get a list of all filenames in the target directory
    for filename in os.listdir(abs_directory):
        # Get the full path to the specific file or directory
        file_path = os.path.join(abs_directory, filename)

        # Check if the path points to a directory
        is_dir=os.path.isdir(file_path)

        # Get the size of the file in bytes
        file_size=os.path.getsize(file_path)

        # Append the formatted info for this file to the response string
        final_response+=f"-{filename}: file_size={file_size} bytes, is_directory={is_dir}\n"
    
    # Return the complete list
    return final_response

# --- Schema Definition for Gemini API ---

# This object defines the 'get_files_info' function *for the AI model*.
# It tells the model what the function is called, what it does, and what
# parameters (arguments) it expects.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info", # A clear description for the model to understand *when* to use this tool
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # Define the 'directory' parameter
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        # Note: 'working_directory' is not defined here, as it's passed
        # from the script's environment, not by the AI model.
    ),
)
