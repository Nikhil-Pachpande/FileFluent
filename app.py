import os
import zipfile
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
from converterFactory import ConverterFactory
from utils import check_file_exists, create_output_directory, validate_file_format, extract_zip, create_zip

app = Flask(__name__)

# Set maximum file size (500 MB)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Allowed extensions for input and output files
ALLOWED_EXTENSIONS = {'txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif'}


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_file():
    # Check if file is provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if file is allowed
    if file and allowed_file(file.filename):
        output_format = request.form.get('output_format')

        # Validate file format
        is_valid, error_message = validate_file_format(file, output_format)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Save the uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join('input', filename)
        file.save(input_path)

        # Prepare the output file path
        output_filename = f"output/{os.path.splitext(filename)[0]}_converted.{output_format}"
        create_output_directory(output_filename)

        # Get the appropriate converter
        try:
            input_format = filename.rsplit('.', 1)[1].lower()
            converter = ConverterFactory.get_converter(input_format, output_format)
            converter.convert(input_path, output_filename)

            return send_file(output_filename, as_attachment=True)

        except Exception as e:
            return jsonify({'error': f"Error during conversion: {e}"}), 500
    else:
        return jsonify({'error': 'File not allowed or invalid'}), 400


@app.route('/convert_zip', methods=['POST'])
def convert_zip():
    # Check if the file is provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file is a zip file
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'Please upload a zip file'}), 400

    output_format = request.form.get('output_format')
    if not output_format:
        return jsonify({'error': 'No output format specified'}), 400

    zip_filename = secure_filename(file.filename)
    zip_path = os.path.join('input', zip_filename)
    file.save(zip_path)

    # Extract the files from the zip archive
    try:
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
        return send_file(converted_zip, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f"Error during batch conversion: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
