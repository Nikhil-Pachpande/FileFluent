import os
import zipfile
import streamlit as st
from converterFactory import ConverterFactory
from utils import check_file_exists, create_output_directory, validate_file_format, extract_zip, create_zip
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS

# Set the maximum file size to 200MB
MAX_FILE_SIZE = 200 * 1024 * 1024

# Streamlit file upload handler
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=SUPPORTED_INPUT_FORMATS, label_visibility="collapsed")
    return uploaded_file

# Function for single file conversion
def convert_single_file(input_file, output_format):
    # Validate file size
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 200MB limit.")
        return

    # Validate file format
    is_valid, error_message = validate_file_format(input_file, output_format)
    if not is_valid:
        st.error(error_message)
        return

    # Save the uploaded file temporarily
    filename = input_file.name
    input_path = os.path.join('input', filename)
    with open(input_path, 'wb') as f:
        f.write(input_file.getbuffer())

    output_filename = f"output/{os.path.splitext(filename)[0]}_converted.{output_format}"
    create_output_directory(output_filename)

    # Get the appropriate converter
    try:
        input_format = filename.rsplit('.', 1)[1].lower()
        converter = ConverterFactory.get_converter(input_format, output_format)
        converter.convert(input_path, output_filename)

        st.success(f"Conversion successful! Download the file below.")
        st.download_button("Download Converted File", output_filename, file_name=output_filename)
    except Exception as e:
        st.error(f"Error during conversion: {e}")

# Function for batch conversion from ZIP file
def convert_zip(input_file, output_format):
    # Validate file size
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 200MB limit.")
        return

    zip_filename = input_file.name
    zip_path = os.path.join('input', zip_filename)
    with open(zip_path, 'wb') as f:
        f.write(input_file.getbuffer())

    try:
        # Extract files from the uploaded ZIP file
        extracted_files = extract_zip(zip_path)

        # Process and convert the extracted files
        converted_files = []
        for extracted_file in extracted_files:
            input_filename = os.path.basename(extracted_file)
            input_format = input_filename.rsplit('.', 1)[1].lower()
            output_filename = f"output/{os.path.splitext(input_filename)[0]}_converted.{output_format}"
            create_output_directory(output_filename)
            converter = ConverterFactory.get_converter(input_format, output_format)
            converter.convert(extracted_file, output_filename)
            converted_files.append(output_filename)

        # Create a zip file of converted files
        converted_zip = create_zip(converted_files)
        st.success("Batch conversion completed successfully! Download the ZIP below.")
        st.download_button("Download Converted ZIP", converted_zip, file_name=converted_zip)

    except Exception as e:
        st.error(f"Error during batch conversion: {e}")

# Streamlit user interface
def main():
    st.title("FileFluent")
    st.write("Upload your files for conversion")

    # Choose between single file conversion and batch file conversion
    task_type = st.radio("Choose a conversion task", ("Single File Conversion", "Batch Conversion (ZIP)"))

    if task_type == "Single File Conversion":
        uploaded_file = upload_file()
        if uploaded_file is not None:
            output_format = st.selectbox("Choose the output format", SUPPORTED_OUTPUT_FORMATS)
            convert_single_file(uploaded_file, output_format)

    elif task_type == "Batch Conversion (ZIP)":
        uploaded_zip = st.file_uploader("Choose a ZIP file", type="zip", label_visibility="collapsed")
        if uploaded_zip is not None:
            output_format = st.selectbox("Choose the output format", SUPPORTED_OUTPUT_FORMATS)
            convert_zip(uploaded_zip, output_format)

if __name__ == "__main__":
    main()
