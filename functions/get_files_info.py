import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_working_path = os.path.abspath(working_directory)
        full_abs = os.path.abspath(full_path)

        if not full_abs.startswith(abs_working_path + os.sep) and full_abs != abs_working_path:
            return f'Error: "{directory}" is outside the working directory.'

        if not os.path.isdir(full_abs):
            return f'Error: "{directory}" is not a directory'

        lines = [f"Result for '{directory}' directory:"]

        for file in os.listdir(full_abs):
            file_path = os.path.join(full_abs, file)
            lines.append(
                f" - {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
            )

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
