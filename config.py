import os
from pathlib import Path

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024

SUPPORTED_INPUT_FORMATS = ['txt', 'csv', 'jpg', 'jpeg', 'png', 'pdf', 'docx', 'xml', 'bmp', 'gif']
SUPPORTED_OUTPUT_FORMATS = ['csv', 'json', 'txt', 'xml', 'png', 'bmp', 'gif', 'docx', 'pdf', 'jpg', 'jpeg']

INPUT_DIR = Path('input')
OUTPUT_DIR = Path('output')

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
