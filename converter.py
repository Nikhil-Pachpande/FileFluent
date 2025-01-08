from PIL import Image
import fitz
import pandas as pd
from docx import Document
import json
import csv
import xml.etree.ElementTree as ET


class Converter:
    def __init__(self, input_path, output_path, output_format):
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    def convert_image(self):
        with Image.open(self.input_path) as img:
            img.save(self.output_path, format=self.output_format.upper())

    def convert_pdf(self):
        doc = fitz.open(self.input_path)
        if self.output_format == 'txt':
            with open(self.output_path, 'w') as txt_file:
                for page in doc:
                    txt_file.write(page.get_text())
        elif self.output_format == 'png':
            page = doc.load_page(0)
            pix = page.get_pixmap()
            pix.save(self.output_path)

    def convert_docx(self):
        doc = Document(self.input_path)
        if self.output_format == 'txt':
            with open(self.output_path, 'w') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')

    def convert_text(self):
        with open(self.input_path, 'r') as txt_file:
            lines = txt_file.readlines()
        if self.output_format == 'json':
            with open(self.output_path, 'w') as json_file:
                json.dump([{"line": line.strip()} for line in lines], json_file)

    def convert(self):
        if self.input_path.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            self.convert_image()
        elif self.input_path.endswith('pdf'):
            self.convert_pdf()
        elif self.input_path.endswith('docx'):
            self.convert_docx()
        elif self.input_path.endswith('txt'):
            self.convert_text()
