from PIL import Image
import fitz
import pandas as pd
from docx import Document
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


    # conversion for docx to text
    def convert_docx(self):
        """Convert DOCX to text (or other formats)."""
        if self.output_format.lower() == 'txt':
            doc = Document(self.input_path)
            with open(self.output_path, 'w') as txt_file:
                for para in doc.paragraphs:
                    txt_file.write(para.text + '\n')
        else:
            raise ValueError(f"Unsupported DOCX output format: {self.output_format}")


    # conversion for csv to json
    def convert_csv(self):
        if self.output_format.lower() == 'json':
            df = pd.read_csv(self.input_path)
            df.to_json(self.output_path, orient='records', lines=True)
        elif self.output_format.lower() == 'txt':
            df = pd.read_csv(self.input_path)
            df.to_csv(self.output_path, index=False, sep='\t')
        else:
            raise ValueError(f"Unsupported CSV output format: {self.output_format}")

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
        else:
            raise ValueError(f"Unsupported input format: {input_format}")
