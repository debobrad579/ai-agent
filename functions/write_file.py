import os

from .utils import outside_working_directory

def write_file(working_directory, file_path, content):
    try:
        if outside_working_directory(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        with open(abs_file_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
