import os


def outside_working_directory(working_directory, file_path):
    abs_directory_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    abs_directory_path = os.path.normpath(abs_directory_path)
    abs_file_path = os.path.normpath(abs_file_path)

    return not abs_file_path.startswith(abs_directory_path + os.sep)
