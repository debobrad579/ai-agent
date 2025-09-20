import os

from .utils import outside_working_directory
from .config import FILE_TRUNCATE_LENGTH


def get_file_content(working_directory, file_path):
    try:
        if outside_working_directory(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as file:
            contents = file.read()
            if len(contents) > FILE_TRUNCATE_LENGTH:
                return contents[:FILE_TRUNCATE_LENGTH] + f'[...File "{file_path}" truncated at {FILE_TRUNCATE_LENGTH} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"
