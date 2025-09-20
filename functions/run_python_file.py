import os
import subprocess
from .utils import outside_working_directory


def run_python_file(working_directory, file_path, args=[]):
    try:
        if outside_working_directory(working_directory, file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        with open(abs_file_path, "rb") as file:
            if not args:
                args = ["python3", abs_file_path]
            else:
                args = ["python3", abs_file_path] + args

            complete_process = subprocess.run(
                args=args,
                input=file.read(),
                capture_output=True,
                timeout=30,
            )

            if not complete_process.stdout and not complete_process.stderr:
                return "No output produced"

            lines = []

            if complete_process.stdout:
                lines.append(f"STDOUT: {complete_process.stdout.decode()}")
            if complete_process.stderr:
                lines.append(f"STDERR: {complete_process.stderr.decode()}")
            if complete_process.returncode:
                lines.append(f"Process exited with status code {complete_process.returncode}")

            return "\n".join(lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"

