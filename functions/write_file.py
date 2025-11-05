import os # Import the 'os' module for path manipulation, directory creation, and validation
from google.genai import types # Import the 'types' from the Google Gemini library to define the function schema


def write_file(working_directory, file_path, content):
    """
    Safely writes content to a file within a specified working directory.

    Performs security checks to prevent directory traversal.
    Automatically creates parent directories if they don't exist.
    Will *not* overwrite a directory.

    Args:
        working_directory (str): The base directory where operations are allowed.
        file_path (str): The relative path to the file to be written.
        content (str): The string content to write to the file.

    Returns:
        str: A success message or an error message.
    """
    
    # --- Security & Path Validation ---
    
    # Get the full, absolute path of the allowed working directory
    abs_working_directory=os.path.abspath(working_directory)

    # Get the full, absolute path of the file the user *wants* to write
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))

    # **Critical Security Check**:
    # Prevent directory traversal attacks.
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # Get the directory that *contains* the file
    parent_dir = os.path.dirname(abs_file_path)
    
    # --- Directory Creation ---
    try:
        # Attempt to create all necessary parent directories.
        # 'exist_ok=True' prevents an error if the directories already exist.
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        # Handle potential errors during directory creation
        return f'Error creating directory "{parent_dir}": {e}'

    # --- File Writing ---

    # check that the file path is not a directory
    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        # Open the file in "w" (write) mode.
        # This will create the file if it doesn't exist,
        # or *overwrite* it completely if it does.
        with open(abs_file_path, "w") as f:
            f.write(content)
        
        # Return a success message if the write completes
        return f'Success: Content written to "{file_path}"'
    except Exception as e:
        # Handle errors during the file writing process
        return f'Error writing to file "{file_path}": {e}'


# --- Schema Definition for Gemini API ---

# This object defines the 'write_file' function *for the AI model*.
schema_write_file = types.FunctionDeclaration(
    # The name *must* match the Python function name exactly
    name="write_file",
    # A clear description for the model
    description="Overwrites an existing file or writes to a new file if it doesn't exist(and creates the parent dirs safely), constrained to the working directory.",
    # Define the parameters the function accepts
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string.",
            ),
        },
    ),
)