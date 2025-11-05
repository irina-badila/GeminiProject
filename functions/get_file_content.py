import os # Import the 'os' module for operating system dependent functionality
from config import MAX_CHARS
from google.genai import types # Import the 'types' from the Google Gemini library to define the function schema

def get_file_content(working_directory, file_path):
    """
    Safely reads the content of a file from within a specified working directory.

    Performs security checks to prevent directory traversal (e.g., accessing "../../etc/passwd")
    and truncates the file content if it exceeds MAX_CHARS.

    Args:
        working_directory (str): The base directory where operations are allowed.
        file_path (str): The relative path to the file to be read.

    Returns:
        str: The file's content (potentially truncated) or an error message.
    """

    # --- Security & Validation Checks ---
    
    # Get the full, absolute path of the allowed working directory
    abs_working_directory=os.path.abspath(working_directory)

    # Get the full, absolute path of the file the user *wants* to read
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    
    # **Critical Security Check**:
    # Ensure the requested file's absolute path *starts with* the working directory's path.
    # This prevents directory traversal attacks (e.g., using "../").
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the path actually exists and is a file (not a directory)
    if not os.path.isfile(abs_file_path):
        return f'Error: file not found or is not a regular file: "{file_path}"'
    
    # --- File Reading ---

    content="" # Initialize empty content string
    try:
        # Open the file in read mode ("r")
        with open(abs_file_path, "r") as f:
            # Read *at most* MAX_CHARS from the file.
            content = f.read(MAX_CHARS)

            # Check if the file was larger than the read limit
            if os.path.getsize(abs_file_path)>MAX_CHARS:
                # If so, append a truncation message to the content
                content+=(f'...File"{file_path}" truncanted at {MAX_CHARS} characters')
            
            # Return the content (either full or truncated)
            return content
    except Exception as e:
        # Handle any potential errors during file opening or reading
        return f'Error reading file "{file_path}": {e}'


# --- Schema Definition for Gemini API ---

# This object defines the 'get_file_content' function *for the AI model*.
# It tells the model what the function is called, what it does, and what
# parameters (arguments) it expects.    
schema_get_files_content = types.FunctionDeclaration(
    # The name *must* match the Python function name exactly
    name="get_file_content",
    # A clear description for the model to understand *when* to use this tool
    description="Retrieves the content of a specific file, constrained to the working directory.",
    # Define the parameters the function accepts
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # Define the 'file_path' parameter
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
        # Note: The 'working_directory' parameter is *not* defined here.
        # This implies it's probably passed to the function from the
        # Python script's environment, not by the AI model itself.
    ),
)