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
        """
        To initialize the converter with input file, output file, and desired output format.

        Parameters:
            input_path (str): Path to the input file.
            output_path (str): Path to save the converted file.
            output_format (str): Desired output format.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    def convert_image(self):
        """
        To convert images between supported formats.

        Supported Input Formats:
            - jpg, jpeg, png, bmp, gif

        Supported Output Formats:
            - jpg, jpeg, png, bmp, gif

        Returns:
            None: Saves the converted image to the specified output path.
        """
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

    def convert_pdf(self):
        """
        To convert PDFs to text, images, or DOCX.

        Returns:
                None: Saves the converted file to the specified output path.
        """
        if self.output_format.lower() == 'txt':
            self.convert_pdf_to_txt()
        elif self.output_format.lower() == 'png':
            self.convert_pdf_to_png()
        elif self.output_format.lower() == 'docx':
            self.convert_pdf_to_docx()
        else:
            raise ValueError(f"Unsupported PDF output format: {self.output_format}")

    def convert_pdf_to_txt(self):
        """
        To extract text content from a PDF.

        Returns:
            None: Saves the extracted text to the specified output path.
        """
        doc = fitz.open(self.input_path)
        with open(self.output_path, 'w') as txt_file:
            for page in doc:
                txt_file.write(page.get_text())

    def convert_pdf_to_png(self):
        """
        To convert the first page of a PDF to an image.

        Returns:
            None: Saves the image to the specified output path.
        """
        doc = fitz.open(self.input_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(self.output_path)

    def convert_pdf_to_docx(self):
        """
        To convert the content of a PDF to a DOCX file.

        Returns:
            None: Saves the DOCX file to the specified output path.
        """
        doc = fitz.open(self.input_path)
        word_doc = Document()

        for page_num, page in enumerate(doc):
            text = page.get_text()
            word_doc.add_paragraph(f"Page {page_num + 1}")
            word_doc.add_paragraph(text)
            word_doc.add_paragraph("\n" + "-" * 50 + "\n")

        word_doc.save(self.output_path)

    def convert_docx(self):
        """
        To convert DOCX files to text or PDF.

        Returns:
            None: Saves the converted file to the specified output path.
        """
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

    def convert_csv(self):
        """
        To convert CSV files to JSON or text.

        Returns:
            None: Saves the converted file to the specified output path.
        """
        if self.output_format.lower() == 'json':
            df = pd.read_csv(self.input_path)
            df.to_json(self.output_path, orient='records', lines=True)
        elif self.output_format.lower() == 'txt':
            df = pd.read_csv(self.input_path)
            df.to_csv(self.output_path, index=False, sep='\t')
        else:
            raise ValueError(f"Unsupported CSV output format: {self.output_format}")

    def convert_text(self):
        """
        To convert plain text files to JSON, CSV, XML, or DOCX.

        Returns:
            None: Saves the converted file to the specified output path.
        """
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

    def convert(self):
        """
        General method to call the appropriate converter based on the input file type.

        Supported Input Formats:
            - Image: jpg, jpeg, png, bmp, gif
            - PDF: pdf
            - Document: docx
            - Text: txt
            - CSV: csv

        Returns:
            None: Calls the relevant conversion method and saves the output.
        """
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
