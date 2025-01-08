import os
import zipfile
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS


def check_file_exists(file_path):
    return os.path.exists(file_path)


def create_output_directory(output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def validate_file_format(input_file, output_format):
    input_format = input_file.name.rsplit('.', 1)[1].lower()

    if input_format not in SUPPORTED_INPUT_FORMATS:
        return False, f"Invalid input format: {input_format}. Allowed formats: {', '.join(SUPPORTED_INPUT_FORMATS)}."

    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        return False, f"Invalid output format: {output_format}. Allowed formats: {', '.join(SUPPORTED_OUTPUT_FORMATS)}."

    return True, ""


def extract_zip(zip_path):
    # Extract files from a zip archive and return the list of extracted file paths.
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('input')
        extracted_files = [os.path.join('input', file) for file in zip_ref.namelist()]
    return extracted_files


def create_zip(files):
    # Create a zip archive containing the converted files.
    zip_filename = "output/converted_files.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_filename
