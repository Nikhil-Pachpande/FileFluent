import os
from PIL import Image
import zipfile
import fitz
import pandas as pd
from docx import Document
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


# Convert image formats (JPEG, PNG, BMP, GIF, etc.)
def convert_image(input_path, output_path, output_format):
    with Image.open(input_path) as img:
        if output_format.lower() == 'png':
            img = img.convert("RGBA")  # Convert image to RGBA mode if converting to PNG
            img.save(output_path, format="PNG")
        elif output_format.lower() == 'jpg' or output_format.lower() == 'jpeg':
            img = img.convert("RGB")  # Convert image to RGB mode if converting to JPEG
            img.save(output_path, format="JPEG")
        elif output_format.lower() == 'bmp':
            img.save(output_path, format="BMP")
        elif output_format.lower() == 'gif':
            img.save(output_path, format="GIF")
        else:
            raise ValueError(f"Unsupported image output format: {output_format}")


# Convert PDF to image (PNG) or text
def convert_pdf(input_path, output_path, output_format):
    """Convert PDF to image (PNG) or text."""
    doc = fitz.open(input_path)
    if output_format.lower() == 'txt':
        with open(output_path, 'w') as txt_file:
            for page in doc:
                txt_file.write(page.get_text())
    elif output_format.lower() == 'png':
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(output_path)
    else:
        raise ValueError(f"Unsupported PDF output format: {output_format}")


# Convert DOCX to text
def convert_docx(input_path, output_path, output_format):
    """Convert DOCX to text or other formats."""
    if output_format.lower() == 'txt':
        doc = Document(input_path)
        with open(output_path, 'w') as txt_file:
            for para in doc.paragraphs:
                txt_file.write(para.text + '\n')
    else:
        raise ValueError(f"Unsupported DOCX output format: {output_format}")


# Convert CSV to JSON
def convert_csv(input_path, output_path, output_format):
    """Convert CSV to JSON or other formats."""
    if output_format.lower() == 'json':
        df = pd.read_csv(input_path)
        df.to_json(output_path, orient='records', lines=True)
    elif output_format.lower() == 'txt':
        df = pd.read_csv(input_path)
        df.to_csv(output_path, index=False, sep='\t')
    else:
        raise ValueError(f"Unsupported CSV output format: {output_format}")


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
