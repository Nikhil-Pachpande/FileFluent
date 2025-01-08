import os

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024

SUPPORTED_INPUT_FORMATS = ['txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif']
SUPPORTED_OUTPUT_FORMATS = ['csv', 'json', 'txt', 'xml', 'png', 'bmp', 'gif', 'docx', 'pdf', 'jpg', 'jpeg']

INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
