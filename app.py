import os
import zipfile
import streamlit as st
from converterFactory import ConverterFactory
from utils import check_file_exists, create_output_directory, validate_file_format, extract_zip, create_zip, convert_image, convert_pdf, convert_docx, convert_csv
from config import SUPPORTED_INPUT_FORMATS, SUPPORTED_OUTPUT_FORMATS, MAX_FILE_SIZE


# to classify the file based on its extension
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


# handle file uploads
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=SUPPORTED_INPUT_FORMATS, label_visibility="collapsed")
    return uploaded_file


# single file conversion
def convert_single_file(input_file, output_format):
    # Validate file size
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    # validate file format
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

    try:
        input_format = filename.rsplit('.', 1)[1].lower()

        # conversion based on input file format
        if input_format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            convert_image(input_path, output_filename, output_format)
        elif input_format == 'pdf':
            convert_pdf(input_path, output_filename, output_format)
        elif input_format == 'docx':
            convert_docx(input_path, output_filename, output_format)
        elif input_format == 'csv':
            convert_csv(input_path, output_filename, output_format)
        else:
            st.error(f"Unsupported conversion for {input_format} to {output_format}.")
            return

        st.success(f"Conversion successful! Download the file below.")
        st.download_button("Download Converted File", output_filename, file_name=output_filename)

    except Exception as e:
        st.error(f"Error during conversion: {e}")


# batch conversion from ZIP file
def convert_zip(input_file, output_format):
    # Validate file size
    if input_file.size > MAX_FILE_SIZE:
        st.error("File size exceeds 1GB limit.")
        return

    zip_filename = input_file.name
    zip_path = os.path.join('input', zip_filename)
    with open(zip_path, 'wb') as f:
        f.write(input_file.getbuffer())

    try:
        # extract files from the uploaded ZIP file
        extracted_files = extract_zip(zip_path)

        # process and convert the extracted files
        converted_files = []
        for extracted_file in extracted_files:
            input_filename = os.path.basename(extracted_file)
            input_format = input_filename.rsplit('.', 1)[1].lower()

            output_filename = f"output/{os.path.splitext(input_filename)[0]}_converted.{output_format}"

            # Convert based on input file format
            if input_format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                convert_image(extracted_file, output_filename, output_format)
            elif input_format == 'pdf':
                convert_pdf(extracted_file, output_filename, output_format)
            elif input_format == 'docx':
                convert_docx(extracted_file, output_filename, output_format)
            elif input_format == 'csv':
                convert_csv(extracted_file, output_filename, output_format)
            else:
                st.error(f"Skipping unsupported file: {input_filename}")
                continue

            converted_files.append(output_filename)

        # create a zip file of converted files
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
            # to classify the uploaded file
            file_type = classify_file(uploaded_file)

            # based on the uploaded file type, show only the appropriate output formats available for conversion
            if file_type == 'image':
                output_formats = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
            elif file_type == 'text':
                output_formats = ['txt', 'json', 'csv', 'xml']
            elif file_type == 'document':
                output_formats = ['pdf', 'txt', 'docx']
            else:
                output_formats = SUPPORTED_OUTPUT_FORMATS  # allow all formats for other types

            output_format = st.selectbox("Choose the output format", output_formats)
            convert_single_file(uploaded_file, output_format)

    elif task_type == "Batch Conversion (ZIP)":
        uploaded_zip = st.file_uploader("Choose a ZIP file", type="zip", label_visibility="collapsed")
        if uploaded_zip is not None:
            # to classify the uploaded ZIP file
            file_type = classify_file(uploaded_zip)

            # based on the uploaded file type, show only the appropriate output formats available for conversion
            if file_type == 'image':
                output_formats = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
            elif file_type == 'text':
                output_formats = ['txt', 'json', 'csv', 'xml']
            elif file_type == 'document':
                output_formats = ['pdf', 'txt', 'docx']
            else:
                output_formats = SUPPORTED_OUTPUT_FORMATS  # Allow all formats for other types

            output_format = st.selectbox("Choose the output format", output_formats)
            convert_zip(uploaded_zip, output_format)


if __name__ == "__main__":
    main()
