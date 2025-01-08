import os
import zipfile
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS


def check_file_exists(file_path):
    """
    To check whether the given file path exists.

    Parameters:
        file_path (str): The file path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def create_output_directory(output_file):
    """
    To ensure that the directory for the output file exists.

    Parameters:
        output_file (str): The path to the output file.

    Returns:
        None
    """
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def validate_file_format(input_file, output_format):
    """
    To validate whether the input file and the desired output format are supported.

    Parameters:
        input_file (UploadedFile): The file to validate.
        output_format (str): The desired output format.

    Returns:
        tuple: (bool, str):
            - `True` if both formats are valid, otherwise `False`.
            - Error message if validation fails, otherwise an empty string.
    """
    input_format = input_file.name.rsplit('.', 1)[1].lower()

    if input_format not in SUPPORTED_INPUT_FORMATS:
        return False, f"Invalid input format: {input_format}. Allowed formats: {', '.join(SUPPORTED_INPUT_FORMATS)}."

    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        return False, f"Invalid output format: {output_format}. Allowed formats: {', '.join(SUPPORTED_OUTPUT_FORMATS)}."

    return True, ""


def extract_zip(zip_path):
    """
    To extract files from a ZIP archive.

    Parameters:
        zip_path (str): The file path of the ZIP archive.

    Returns:
        list: A list of file paths for the extracted files.
    """
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('input')
        extracted_files = [os.path.join('input', file) for file in zip_ref.namelist()]
    return extracted_files


def create_zip(files):
    """
    To create a ZIP archive containing the provided files.

    Parameters:
        files (list): A list of file paths to include in the ZIP archive.

    Returns:
        str: The file path of the created ZIP archive.
    """
    zip_filename = "output/converted_files.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_filename
