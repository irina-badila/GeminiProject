import os

def get_files_info(working_directory: str, directory="."):
    abs_working_directory=os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_directory.startswith(abs_working_directory):
        return f"Error: Cannot list '{directory}': directory as it is outside the working directory"
    final_response="";
    for filename in os.listdir(abs_directory):
        file_path = os.path.join(abs_directory, filename)
        is_dir=os.path.isdir(file_path)
        file_size=os.path.getsize(file_path)
        final_response+=f"-{filename}: file_size={file_size} bytes, is_directory={is_dir}\n"
    return final_response

