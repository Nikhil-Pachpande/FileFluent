import os
import streamlit as st
from converterFactory import ConverterFactory
from utils import validate_file_format, create_output_directory, extract_zip, create_zip
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS, MAX_FILE_SIZE


def classify_file(input_file):
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


def convert_single_file(input_file, output_format):
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    is_valid, error_message = validate_file_format(input_file, output_format)
    if not is_valid:
        st.error(error_message)
        return

    input_path = os.path.join('input', input_file.name)
    with open(input_path, 'wb') as f:
        f.write(input_file.getbuffer())

    output_filename = f"{os.path.splitext(input_file.name)[0]}_converted.{output_format}"
    output_path = os.path.join('output', output_filename)
    create_output_directory(output_path)

    try:
        input_format = input_file.name.rsplit('.', 1)[1].lower()
        converter = ConverterFactory.get_converter(input_format, output_format, input_path, output_path)
        converter.convert()
        st.success("Conversion successful! Download the file below.")
        st.download_button("Download Converted File", open(output_path, 'rb'), file_name=output_filename)
    except Exception as e:
        st.error(f"Error during conversion: {e}")


def convert_zip(input_file, output_format):
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    zip_path = os.path.join('input', input_file.name)
    with open(zip_path, 'wb') as f:
        f.write(input_file.getbuffer())

    try:
        extracted_files = extract_zip(zip_path)
        converted_files = []

        for extracted_file in extracted_files:
            input_filename = os.path.basename(extracted_file)
            input_format = input_filename.rsplit('.', 1)[1].lower()
            output_filename = f"{os.path.splitext(input_filename)[0]}_converted.{output_format}"
            output_path = os.path.join('output', output_filename)

            converter = ConverterFactory.get_converter(input_format, output_format, extracted_file, output_path)
            converter.convert()
            converted_files.append(output_path)

        converted_zip = create_zip(converted_files)
        st.success("Batch conversion completed successfully! Download the ZIP below.")
        st.download_button("Download Converted ZIP", open(converted_zip, 'rb'), file_name='converted_files.zip')
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

            output_format = st.selectbox("Choose the output format", [fmt for fmt in output_formats if fmt != uploaded_file.name.rsplit('.', 1)[1].lower()])

            if st.button("Convert"):
                convert_single_file(uploaded_file, output_format)

    elif task_type == "Batch Conversion (ZIP)":
        uploaded_zip = st.file_uploader("Choose a ZIP file", type="zip", label_visibility="collapsed")
        if uploaded_zip:
            output_formats = SUPPORTED_OUTPUT_FORMATS
            output_format = st.selectbox("Choose the output format", output_formats)

            if st.button("Convert"):
                convert_zip(uploaded_zip, output_format)


if __name__ == "__main__":
    main()
