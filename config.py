import os

# List of supported input file formats
SUPPORTED_INPUT_FORMATS = ['txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif']

# List of supported output file formats
SUPPORTED_OUTPUT_FORMATS = ['csv', 'json', 'txt', 'xml', 'png', 'bmp', 'gif', 'docx', 'pdf']

# Maximum file size in bytes (500MB)
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB

# Allowed file extensions for validation
ALLOWED_EXTENSIONS = {'txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif'}

# Directory paths for input and output files
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

# Create the directories if they don't exist
if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
