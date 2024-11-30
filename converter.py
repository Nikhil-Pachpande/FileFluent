from PIL import Image
import fitz
import pandas as pd
from docx import Document
import json
import csv
import xml.etree.ElementTree as ET
import subprocess
from config import SUPPORTED_INPUT_FORMATS


class Converter:
    def __init__(self, input_path, output_path, output_format):
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    # conversion for any input image format to any other supported format
    def convert_image(self):
        with Image.open(self.input_path) as img:
            if self.output_format.lower() == 'png':
                img = img.convert("RGBA")
                img.save(self.output_path, format="PNG")
            elif self.output_format.lower() in ['jpg', 'jpeg']:
                img = img.convert("RGB")
                img.save(self.output_path, format="JPEG")
            elif self.output_format.lower() == 'bmp':
                img.save(self.output_path, format="BMP")
            elif self.output_format.lower() == 'gif':
                img.save(self.output_path, format="GIF")
            else:
                raise ValueError(f"Unsupported image output format: {self.output_format}")

    # conversion for pdf to text/png
    def convert_pdf(self):
        doc = fitz.open(self.input_path)
        if self.output_format.lower() == 'txt':
            with open(self.output_path, 'w') as txt_file:
                for page in doc:
                    txt_file.write(page.get_text())
        elif self.output_format.lower() == 'png':
            page = doc.load_page(0)
            pix = page.get_pixmap()
            pix.save(self.output_path)
        else:
            raise ValueError(f"Unsupported PDF output format: {self.output_format}")

    # conversion for docx to text/pdf
    def convert_docx(self):
        if self.output_format.lower() == 'txt':
            doc = Document(self.input_path)
            with open(self.output_path, 'w') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')
        elif self.output_format.lower() == 'pdf':
            self.convert_docx_to_pdf()  # Convert DOCX to PDF using LibreOffice
        else:
            raise ValueError(f"Unsupported DOCX output format: {self.output_format}")

    # conversion for docx to pdf
    def convert_docx_to_pdf(self):
        try:
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', self.input_path],
                           check=True)
            output_pdf_path = self.input_path.replace('.docx', '.pdf')
            subprocess.run(['mv', output_pdf_path, self.output_path], check=True)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to convert DOCX to PDF: {e}")

    # conversion csv to json/txt
    def convert_csv(self):
        if self.output_format.lower() == 'json':
            df = pd.read_csv(self.input_path)
            df.to_json(self.output_path, orient='records', lines=True)
        elif self.output_format.lower() == 'txt':
            df = pd.read_csv(self.input_path)
            df.to_csv(self.output_path, index=False, sep='\t')
        else:
            raise ValueError(f"Unsupported CSV output format: {self.output_format}")

    # conversion text to json/csv/xml/docx
    def convert_text(self):
        if self.output_format.lower() == 'json':
            self.convert_text_to_json()
        elif self.output_format.lower() == 'csv':
            self.convert_text_to_csv()
        elif self.output_format.lower() == 'xml':
            self.convert_text_to_xml()
        elif self.output_format.lower() == 'docx':
            self.convert_text_to_docx()
        else:
            raise ValueError(f"Unsupported text output format: {self.output_format}")

    # conversion text to json
    def convert_text_to_json(self):
        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        data = []
        for line in lines:
            data.append({"text": line.strip()})

        with open(self.output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    # conversion text to csv
    def convert_text_to_csv(self):
        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        rows = [line.strip().split(' ') for line in lines]

        with open(self.output_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    # conversion text to xml
    def convert_text_to_xml(self):
        root = ET.Element("root")

        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            item = ET.SubElement(root, "item", id=str(i + 1))
            item.text = line.strip()

        tree = ET.ElementTree(root)
        tree.write(self.output_path)

    # conversion text to docx
    def convert_text_to_docx(self):
        doc = Document()

        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            doc.add_paragraph(line.strip())

        doc.save(self.output_path)

    # general method to call respective converter to the input file format
    def convert(self):
        input_format = self.input_path.split('.')[-1].lower()

        if input_format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            self.convert_image()
        elif input_format == 'pdf':
            self.convert_pdf()
        elif input_format == 'docx':
            self.convert_docx()
        elif input_format == 'csv':
            self.convert_csv()
        elif input_format == 'txt':
            self.convert_text()
        else:
            raise ValueError(f"Unsupported input format: {input_format}")
