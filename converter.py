from PIL import Image
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
import csv
import os
import xml.etree.ElementTree as ET


class Converter:
    def __init__(self, input_path, output_path, output_format):
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    # Convert images to various formats
    def convert_image(self):
        with Image.open(self.input_path) as img:
            if self.output_format.lower() == 'png':
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

    # Convert PDFs to text or images
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

    # Convert DOCX to text or PDF
    def convert_docx(self):
        if self.output_format.lower() == 'txt':
            self.convert_docx_to_txt()
        elif self.output_format.lower() == 'pdf':
            self.convert_docx_to_pdf()
        else:
            raise ValueError(f"Unsupported DOCX output format: {self.output_format}")

    def convert_docx_to_txt(self):
        doc = Document(self.input_path)
        with open(self.output_path, 'w') as txt_file:
            for para in doc.paragraphs:
                txt_file.write(para.text + '\n')

    def convert_docx_to_pdf(self):
        doc = Document(self.input_path)
        c = canvas.Canvas(self.output_path, pagesize=letter)
        width, height = letter
        y_position = height - 50  # Start position for text

        for para in doc.paragraphs:
            text = para.text
            if y_position < 50:  # Add a new page if text exceeds page height
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, text)
            y_position -= 15  # Move down for the next line

        c.save()

    # Convert CSV to JSON or TXT
    def convert_csv(self):
        if self.output_format.lower() == 'json':
            df = pd.read_csv(self.input_path)
            df.to_json(self.output_path, orient='records', lines=True)
        elif self.output_format.lower() == 'txt':
            df = pd.read_csv(self.input_path)
            df.to_csv(self.output_path, index=False, sep='\t')
        else:
            raise ValueError(f"Unsupported CSV output format: {self.output_format}")

    # Convert text to JSON, CSV, XML, or DOCX
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

    def convert_text_to_json(self):
        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        data = [{"line": line.strip()} for line in lines]

        with open(self.output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def convert_text_to_csv(self):
        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        rows = [line.strip().split(' ') for line in lines]

        with open(self.output_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    def convert_text_to_xml(self):
        root = ET.Element("root")

        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            item = ET.SubElement(root, "item", id=str(i + 1))
            item.text = line.strip()

        tree = ET.ElementTree(root)
        tree.write(self.output_path)

    def convert_text_to_docx(self):
        doc = Document()

        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            doc.add_paragraph(line.strip())

        doc.save(self.output_path)

    # General method to call the appropriate converter based on the file type
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
