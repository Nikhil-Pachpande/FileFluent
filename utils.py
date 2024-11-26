import os


def check_file_exists(file_path):
    return os.path.exists(file_path)


def create_output_directory(output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
