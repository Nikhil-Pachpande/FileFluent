from converter import TextToCSVConverter, CSVToJSONConverter, JSONToCSVConverter, JSONToTextConverter, CSVToTextConverter, ImageToImageConverter, PDFToTextConverter, PDFToImageConverter, WordToPDFConverter, PDFToWordConverter, XMLToJSONConverter, JSONToXMLConverter, XMLToCSVConverter, CSVToPDFConverter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format, output_format):
        if input_format == 'txt' and output_format == 'csv':
            return TextToCSVConverter()
        elif input_format == 'csv' and output_format == 'json':
            return CSVToJSONConverter()
        elif input_format == 'json' and output_format == 'csv':
            return JSONToCSVConverter()
        elif input_format == 'json' and output_format == 'txt':
            return JSONToTextConverter()
        elif input_format == 'csv' and output_format == 'txt':
            return CSVToTextConverter()
        elif input_format in ['jpg', 'jpeg'] and output_format in ['png', 'bmp', 'gif']:
            return ImageToImageConverter(output_format)
        elif input_format == 'pdf' and output_format == 'txt':
            return PDFToTextConverter()
        elif input_format == 'pdf' and output_format == 'image':
            return PDFToImageConverter()
        elif input_format == 'docx' and output_format == 'pdf':
            return WordToPDFConverter()
        elif input_format == 'pdf' and output_format == 'docx':
            return PDFToWordConverter()
        elif input_format == 'xml' and output_format == 'json':
            return XMLToJSONConverter()
        elif input_format == 'json' and output_format == 'xml':
            return JSONToXMLConverter()
        elif input_format == 'xml' and output_format == 'csv':
            return XMLToCSVConverter()
        elif input_format == 'csv' and output_format == 'pdf':
            return CSVToPDFConverter()
        else:
            raise ValueError(f"No converter available for {input_format} to {output_format}")
