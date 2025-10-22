import os
def write_file(working_directory, file_path, content):
    abs_working_directory=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    parent_dir = os.path.dirname(abs_file_path)
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f'Error creating directory "{parent_dir}": {e}'

    # check that the file path is not a directory
    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Success: Content written to "{file_path}"'
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'