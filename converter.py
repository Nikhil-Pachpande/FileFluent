import os
from PIL import Image
import fitz
import pandas as pd
from docx import Document
import json
import csv
import xml.etree.ElementTree as ET
import subprocess


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
        if self.output_format == 'txt':
            doc = Document(self.input_path)
            with open(self.output_path, 'w') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')
        elif self.output_format == 'pdf':
            self.convert_docx_to_pdf()
        else:
            raise ValueError(f"Unsupported DOCX output format: {self.output_format}")

    def convert_docx_to_pdf(self):
        try:
            output_dir = os.path.dirname(self.output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, self.input_path],
                check=True
            )
            generated_pdf = os.path.join(output_dir, os.path.splitext(os.path.basename(self.input_path))[0] + '.pdf')
            os.rename(generated_pdf, self.output_path)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to convert DOCX to PDF: {e}")
        except FileNotFoundError as e:
            raise ValueError(f"LibreOffice is not installed or not found: {e}")

    def convert_text(self):
        with open(self.input_path, 'r') as txt_file:
            lines = txt_file.readlines()
        if self.output_format == 'json':
            with open(self.output_path, 'w') as json_file:
                json.dump([{"line": line.strip()} for line in lines], json_file)
        elif self.output_format == 'csv':
            with open(self.output_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for line in lines:
                    writer.writerow([line.strip()])
        else:
            raise ValueError(f"Unsupported text output format: {self.output_format}")

    def convert(self):
        if self.input_path.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            self.convert_image()
        elif self.input_path.endswith('pdf'):
            self.convert_pdf()
        elif self.input_path.endswith('docx'):
            self.convert_docx()
        elif self.input_path.endswith('txt'):
            self.convert_text()
        else:
            raise ValueError(f"Unsupported input format: {os.path.splitext(self.input_path)[1]}")
