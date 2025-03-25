import os
import zipfile
from pathlib import Path
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS


def check_file_exists(file_path: str) -> bool:
    return Path(file_path).exists()


def create_output_directory(output_file: str) -> None:
    output_dir = Path(output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)


def validate_file_format(input_file, output_format: str) -> tuple[bool, str]:
    input_format = input_file.name.split('.')[-1].lower()
    if input_format not in SUPPORTED_INPUT_FORMATS:
        return (
            False,
            f"Invalid input format: {input_format}. Allowed formats: {', '.join(SUPPORTED_INPUT_FORMATS)}."
        )
    if output_format.lower() not in SUPPORTED_OUTPUT_FORMATS:
        return (
            False,
            f"Invalid output format: {output_format}. Allowed formats: {', '.join(SUPPORTED_OUTPUT_FORMATS)}."
        )
    return True, ""


def extract_zip(zip_path: str) -> list:
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extract_path = Path('input')
        zip_ref.extractall(extract_path)
        extracted_files = [str(extract_path / file) for file in zip_ref.namelist()]
    return extracted_files


def create_zip(files: list) -> str:
    zip_filename = Path("output/converted_files.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=Path(file).name)
    return str(zip_filename)
