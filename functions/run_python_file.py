import os
import subprocess
from google.genai import types

def run_python_file(working_directory,file_path:str,args=None):
    abs_working_directory=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(commands, capture_output=True, text=True, timeout=30,cwd=abs_working_directory)
        output=[]
        if result.stdout:
            output.append("STDOUT:")
            output.append(result.stdout)
        if result.stderr:
            output.append("STDERR:")
            output.append(result.stderr)
        return "\n".join(output)
    
        if result.returncode != 0:
            return f'Error: Script "{file_path}" exited with code {result.returncode}'

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f'Error running file "{file_path}": {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file with python3 interpreter. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
            ),
        },
    ),
)