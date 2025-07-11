# FileFluent [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://filefluent.streamlit.app)
FileFluent is a Streamlit-based web application that allows users to convert files between various formats. It supports single file conversions as well as batch conversions via ZIP archives. The app is designed to handle multiple file types, including images, documents, text files, PDFs, and more.
The application is live at https://filefluent.streamlit.app.


## Features
### Single File Conversion
- Convert images (JPG, PNG, BMP, GIF, etc.) between formats.
- Convert PDFs to text, images, or DOCX.
- Convert DOCX files to text or PDF.
- Convert plain text files to JSON, CSV, XML, or DOCX.
- Convert CSV files to JSON or text.

### Batch Conversion
- Upload a ZIP file containing multiple files.
- Convert all files in the ZIP to a specified output format.
- Download the converted files as a ZIP.

### Error Handling
- Validates input and output formats.
- Ensures file size limits (up to 1GB).
- Provides meaningful error messages for unsupported formats or issues during conversion.

## Technologies Used
- Python - for core programming
- Streamlit - for web-based interface
- Pillow - for image processing
- PyMuPDF - for handling PDF files
- python-docx - for handling docx files and related conversions
- pandas - for handling csv and json file conversions
- reportlab - for generating PDFs

## Supported File Types
### Input Formats:
- Images: JPG, JPEG, PNG, BMP, GIF
- Text: TXT
- Documents: DOCX
- PDFs: PDF
- CSV: CSV
### Output Formats:
- Images: PNG, JPG, JPEG, BMP, GIF
- Text: TXT, JSON, XML
- Documents: DOCX, PDF
- CSV: JSON, TXT

## Usage
1. Single File Conversion
- Upload a file.
- Select the desired output format from the dropdown.
- Click the "Convert" button.
- Download the converted file.
2. Batch Conversion
- Upload a ZIP file containing multiple files.
- Select the desired output format for all files.
- Click the "Convert" button.
- Download the ZIP containing the converted files.

## Setup and Installation
- git clone https://github.com/nikhil-pachpande/filefluent.git
- cd filefluent
- pip install -r requirements.txt
- streamlit run app.py
- open localhost in your browser

## Future Enhancements
- Add support for additional file formats (e.g., audio, video).
- Implement OCR for converting scanned PDFs to editable text.
- Allow user-defined output directories.
- Add support for cloud storage integrations (e.g., AWS S3, Google Drive)