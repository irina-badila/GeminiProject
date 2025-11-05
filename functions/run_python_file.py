import os # Import the 'os' module for path manipulation and validation
import subprocess # Import the 'subprocess' module to run external commands
from google.genai import types # Import the 'types' from the Google Gemini library to define the function schema



def run_python_file(working_directory,file_path:str,args=None):
    """
        Safely runs a Python script as a subprocess.

        Performs security checks to ensure the script is within the allowed
        working directory. Captures and returns its standard output and standard error.

        Args:
            working_directory (str): The base directory where operations are allowed.
            file_path (str): The relative path to the .py file to be executed.
            args (list, optional): A list of string arguments to pass to the script.

        Returns:
            str: A formatted string containing the script's STDOUT and STDERR,
                or an error message.
    """
    
    # --- Security & Validation Checks ---

    # Get the full, absolute path of the allowed working directory
    abs_working_directory=os.path.abspath(working_directory)

    # Get the full, absolute path of the script the user *wants* to run
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))

    # **Critical Security Check**:
    # Prevent directory traversal attacks.
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file exists on disk
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    
    # Simple check to ensure it's a Python file.
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    # --- Subprocess Execution ---
    try:
        # Build the command list to be executed. Start with 'python' and the script path.
        commands = ["python", abs_file_path]
        
        # If any command-line arguments are provided, add them to the command list
        if args:
            commands.extend(args)

        # Execute the command
        result = subprocess.run(
                                commands, 
                                capture_output=True,  # Capture STDOUT and STDERR
                                text=True, # Decode STDOUT/STDERR as text (str)
                                timeout=30, # Set a 30-second timeout to prevent hung scripts 
                                cwd=abs_working_directory) # Set the child's CWD to the working dir
        
        # Print the full result object (for debugging on the server side)
        print(result)

        # Prepare the output to be returned
        output=[]
        if result.stdout:
            output.append("STDOUT:")
            output.append(result.stdout)
        if result.stderr:
            output.append("STDERR:")
            output.append(result.stderr)
#        return "\n".join(output)
    
        if result.returncode != 0:
            return f'Error: Script "{file_path}" exited with code {result.returncode}'

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f'Error running file "{file_path}": {e}'

# --- Schema Definition for Gemini API ---

# This object defines the 'run_python_file' function *for the AI model*.   
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file", # The name *must* match the Python function name exactly
    description="Runs a Python file with python3 interpreter. Accepts additional CLI args as an optional array.",
    # Define the parameters the function accepts
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the Python file,",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)