import os

# to handle files upto 1 GB
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024

# supported file formats
SUPPORTED_INPUT_FORMATS = ['txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif']
SUPPORTED_OUTPUT_FORMATS = ['csv', 'json', 'txt', 'xml', 'png', 'bmp', 'gif', 'docx', 'pdf']

# allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif'}

# Input and output directories
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

# create directories if they don't exist
if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
