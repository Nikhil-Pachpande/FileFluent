import streamlit as st

import os
from converterFactory import ConverterFactory
from utils import check_file_exists, create_output_directory
import tempfile


def main():
    st.title("File Converter")

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "json", "pdf", "docx", "jpg", "jpeg", "png", "bmp", "gif", "xml"])

    output_format = st.selectbox("Select Output Format", ["csv", "json", "txt", "pdf", "docx", "png", "bmp", "gif"])

    if uploaded_file is not None and output_format:
        if uploaded_file.type in ["text/plain", "text/csv", "application/json"]:
            try:
                content = uploaded_file.getvalue()
                decoded_content = content.decode("utf-8")
            except UnicodeDecodeError:
                st.error("The file is not encoded in UTF-8. Please upload a UTF-8 encoded file.")
                return

            st.write("Uploaded File Preview:")
            st.write(decoded_content[:500])

        elif uploaded_file.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            st.write("Uploaded file is binary (PDF/Word). No preview available.")

        if st.button("Convert"):
            with tempfile.NamedTemporaryFile(delete=False) as temp_input:
                temp_input.write(uploaded_file.getvalue())
                temp_input.close()

                output_filename = f"output/{os.path.splitext(uploaded_file.name)[0]}_converted.{output_format}"
                create_output_directory(output_filename)

                input_format = uploaded_file.name.split('.')[-1].lower()
                try:
                    converter = ConverterFactory.get_converter(input_format, output_format)
                    converter.convert(temp_input.name, output_filename)

                    with open(output_filename, "rb") as f:
                        st.download_button("Download Converted File", f, file_name=output_filename)

                except Exception as e:
                    st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
