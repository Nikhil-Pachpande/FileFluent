import os
import streamlit as st
from pathlib import Path
from converterFactory import ConverterFactory
from utils import validate_file_format, create_output_directory, extract_zip, create_zip
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS, MAX_FILE_SIZE


def classify_file(input_file) -> str:
    extension = input_file.name.split('.')[-1].lower()
    if extension in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        return 'image'
    elif extension in ['txt', 'csv', 'xml', 'json']:
        return 'text'
    elif extension in ['pdf', 'docx']:
        return 'document'
    else:
        return 'other'


def upload_file():
    return st.file_uploader("Choose a file", type=SUPPORTED_INPUT_FORMATS, label_visibility="collapsed")


def convert_single_file(input_file, output_format: str) -> None:
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    is_valid, error_message = validate_file_format(input_file, output_format)
    if not is_valid:
        st.error(error_message)
        return

    input_path = Path('input') / input_file.name
    with open(input_path, 'wb') as f:
        f.write(input_file.getbuffer())

    output_filename = f"{input_path.stem}_converted.{output_format}"
    output_path = Path('output') / output_filename
    create_output_directory(str(output_path))

    try:
        input_format = input_file.name.split('.')[-1].lower()
        converter = ConverterFactory.get_converter(input_format, output_format, str(input_path), str(output_path))
        converter.convert()
        st.success("Conversion successful! Download the file below.")
        with open(output_path, 'rb') as converted_file:
            st.download_button("Download Converted File", data=converted_file, file_name=output_filename)
    except Exception as e:
        st.error(f"Error during conversion: {e}")


def convert_zip(input_file, output_format: str) -> None:
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    zip_path = Path('input') / input_file.name
    with open(zip_path, 'wb') as f:
        f.write(input_file.getbuffer())

    try:
        extracted_files = extract_zip(str(zip_path))
        converted_files = []

        for file in extracted_files:
            file_path = Path(file)
            input_format = file_path.suffix.lower().lstrip('.')
            output_filename = f"{file_path.stem}_converted.{output_format}"
            output_file = Path('output') / output_filename
            converter = ConverterFactory.get_converter(input_format, output_format, str(file_path), str(output_file))
            converter.convert()
            converted_files.append(str(output_file))

        converted_zip = create_zip(converted_files)
        st.success("Batch conversion completed successfully! Download the ZIP below.")
        with open(converted_zip, 'rb') as zip_file:
            st.download_button("Download Converted ZIP", data=zip_file, file_name='converted_files.zip')
    except Exception as e:
        st.error(f"Error during batch conversion: {e}")


def main():
    st.title("FileFluent")
    st.write("Upload your files for conversion")

    task_type = st.radio("Choose a conversion task", ("Single File Conversion", "Batch Conversion (ZIP)"))

    if task_type == "Single File Conversion":
        uploaded_file = upload_file()
        if uploaded_file:
            file_type = classify_file(uploaded_file)
            if file_type == 'image':
                output_formats = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
            elif file_type == 'text':
                output_formats = ['json', 'csv', 'xml', 'docx']
            elif file_type == 'document':
                output_formats = ['pdf', 'txt', 'docx']
            else:
                output_formats = SUPPORTED_OUTPUT_FORMATS

            # Exclude the input file's format from the selection
            input_ext = uploaded_file.name.split('.')[-1].lower()
            output_formats = [fmt for fmt in output_formats if fmt != input_ext]

            output_format = st.selectbox("Choose the output format", output_formats)

            if st.button("Convert"):
                convert_single_file(uploaded_file, output_format)

    elif task_type == "Batch Conversion (ZIP)":
        uploaded_zip = st.file_uploader("Choose a ZIP file", type="zip", label_visibility="collapsed")
        if uploaded_zip:
            output_format = st.selectbox("Choose the output format", SUPPORTED_OUTPUT_FORMATS)
            if st.button("Convert"):
                convert_zip(uploaded_zip, output_format)


if __name__ == "__main__":
    main()
