from abc import ABC, abstractmethod
import csv
import json
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image
import fitz
from docx2pdf import convert as docx_to_pdf
from PyPDF2 import PdfReader
from docx import Document
from fpdf import FPDF


class FileConverter(ABC):
    @abstractmethod
    def convert(self, input_file, output_file):
        pass


class TextToCSVConverter(FileConverter):
    def convert(self, input_file, output_file):
        with open(input_file, 'r') as txt_file:
            lines = txt_file.readlines()

        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in lines:
                writer.writerow(line.strip().split())


class CSVToJSONConverter(FileConverter):
    def convert(self, input_file, output_file):
        df = pd.read_csv(input_file)
        df.to_json(output_file, orient='records', lines=True)


class JSONToCSVConverter(FileConverter):
    def convert(self, input_file, output_file):
        df = pd.read_json(input_file)
        df.to_csv(output_file, index=False)


class JSONToTextConverter(FileConverter):
    def convert(self, input_file, output_file):
        with open(input_file, 'r') as f:
            data = json.load(f)

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)


class CSVToTextConverter(FileConverter):
    def convert(self, input_file, output_file):
        df = pd.read_csv(input_file)
        df.to_string(output_file, index=False)


class ImageToImageConverter(FileConverter):
    def __init__(self, format):
        self.format = format

    def convert(self, input_file, output_file):
        with Image.open(input_file) as img:
            img.convert('RGB').save(output_file, format=self.format.upper())


class PDFToTextConverter(FileConverter):
    def convert(self, input_file, output_file):
        doc = fitz.open(input_file)
        with open(output_file, 'w') as f:
            for page in doc:
                f.write(page.get_text())


class PDFToImageConverter(FileConverter):
    def convert(self, input_file, output_file):
        doc = fitz.open(input_file)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(output_file)


class WordToPDFConverter(FileConverter):
    def convert(self, input_file, output_file):
        try:
            docx_to_pdf(input_file, output_file)
        except Exception as e:
            raise ValueError(f"Error converting Word to PDF: {e}")


class PDFToWordConverter(FileConverter):
    def convert(self, input_file, output_file):
        try:
            reader = PdfReader(input_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            doc = Document()
            doc.add_paragraph(text)
            doc.save(output_file)
        except Exception as e:
            raise ValueError(f"Error converting PDF to Word: {e}")


class XMLToJSONConverter(FileConverter):
    def convert(self, input_file, output_file):
        tree = ET.parse(input_file)
        root = tree.getroot()

        def parse_element(element):
            data = {}
            for child in element:
                data[child.tag] = parse_element(child) if len(child) > 0 else child.text
            return data

        data = {root.tag: parse_element(root)}

        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)


class JSONToXMLConverter(FileConverter):
    def convert(self, input_file, output_file):
        with open(input_file, 'r') as f:
            data = json.load(f)

        def dict_to_xml(tag, d):
            result = []
            for key, value in d.items():
                if isinstance(value, dict):
                    result.append(f"<{key}>{dict_to_xml(key, value)}</{key}>")
                else:
                    result.append(f"<{key}>{value}</{key}>")
            return ''.join(result)

        xml_data = dict_to_xml('root', data)
        with open(output_file, 'w') as f:
            f.write(xml_data)


class XMLToCSVConverter(FileConverter):
    def convert(self, input_file, output_file):
        tree = ET.parse(input_file)
        root = tree.getroot()
        rows = []

        def parse_element(element):
            data = {}
            for child in element:
                data[child.tag] = parse_element(child) if len(child) > 0 else child.text
            return data

        for item in root:
            rows.append(parse_element(item))

        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False)


class CSVToPDFConverter(FileConverter):
    def convert(self, input_file, output_file):
        df = pd.read_csv(input_file)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        pdf.cell(40, 10, 'Column 1', border=1)
        pdf.cell(40, 10, 'Column 2', border=1)
        pdf.cell(40, 10, 'Column 3', border=1)
        pdf.ln()

        for index, row in df.iterrows():
            pdf.cell(40, 10, str(row[0]), border=1)
            pdf.cell(40, 10, str(row[1]), border=1)
            pdf.cell(40, 10, str(row[2]), border=1)
            pdf.ln()

        pdf.output(output_file)
